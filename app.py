import os
from flask import Flask, render_template_string
import boto3
from botocore.exceptions import BotoCoreError, ClientError

app = Flask(__name__)

REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

ec2_client = boto3.client("ec2", region_name=REGION)
elb_client = boto3.client("elbv2", region_name=REGION)

HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>AWS Mini Dashboard</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 24px; }
    h1 { margin-bottom: 4px; }
    h2 { margin-top: 28px; }
    .grid { display: grid; grid-template-columns: repeat(auto-fit,minmax(340px,1fr)); gap: 18px; }
    table { border-collapse: collapse; width: 100%; }
    th, td { border: 1px solid #ddd; padding: 8px; font-size: 14px; }
    th { background: #f3f3f3; text-align: left; }
    .error { color: #b00020; background:#ffecec; border:1px solid #ffd0d0; padding:10px; }
    small { color:#555; }
  </style>
</head>
<body>
  <h1>AWS Mini Dashboard</h1>
  <small>Region: {{ region }}</small>

  {% if errors %}
    <div class="error">
      <strong>Warnings/Errors:</strong>
      <ul>
        {% for e in errors %}
          <li>{{ e }}</li>
        {% endfor %}
      </ul>
    </div>
  {% endif %}

  <div class="grid">

    <section>
      <h2>EC2 Instances</h2>
      <table>
        <thead><tr><th>ID</th><th>State</th><th>Type</th><th>Public IP</th></tr></thead>
        <tbody>
        {% for i in instance_data %}
          <tr>
            <td>{{ i["ID"] }}</td>
            <td>{{ i["State"] }}</td>
            <td>{{ i["Type"] }}</td>
            <td>{{ i["Public IP"] }}</td>
          </tr>
        {% endfor %}
        {% if instance_data|length == 0 %}
          <tr><td colspan="4"><em>No instances found</em></td></tr>
        {% endif %}
        </tbody>
      </table>
    </section>

    <section>
      <h2>VPCs</h2>
      <table>
        <thead><tr><th>VPC ID</th><th>CIDR</th><th>Is Default</th></tr></thead>
        <tbody>
        {% for v in vpc_data %}
          <tr>
            <td>{{ v["VPC ID"] }}</td>
            <td>{{ v["CIDR"] }}</td>
            <td>{{ v["Default"] }}</td>
          </tr>
        {% endfor %}
        {% if vpc_data|length == 0 %}
          <tr><td colspan="3"><em>No VPCs found</em></td></tr>
        {% endif %}
        </tbody>
      </table>
    </section>

    <section>
      <h2>Load Balancers (ALB/NLB)</h2>
      <table>
        <thead><tr><th>Name</th><th>DNS Name</th><th>Type</th><th>Scheme</th></tr></thead>
        <tbody>
        {% for lb in lb_data %}
          <tr>
            <td>{{ lb["LB Name"] }}</td>
            <td>{{ lb["DNS Name"] }}</td>
            <td>{{ lb["Type"] }}</td>
            <td>{{ lb["Scheme"] }}</td>
          </tr>
        {% endfor %}
        {% if lb_data|length == 0 %}
          <tr><td colspan="4"><em>No Load Balancers found</em></td></tr>
        {% endif %}
        </tbody>
      </table>
    </section>

    <section>
      <h2>AMIs (owned by self)</h2>
      <table>
        <thead><tr><th>AMI ID</th><th>Name</th><th>Created</th></tr></thead>
        <tbody>
        {% for ami in ami_data %}
          <tr>
            <td>{{ ami["AMI ID"] }}</td>
            <td>{{ ami["Name"] }}</td>
            <td>{{ ami["CreationDate"] }}</td>
          </tr>
        {% endfor %}
        {% if ami_data|length == 0 %}
          <tr><td colspan="3"><em>No AMIs found</em></td></tr>
        {% endif %}
        </tbody>
      </table>
      <small>Showing up to {{ ami_limit }} latest.</small>
    </section>

  </div>
</body>
</html>
"""

def _safe(fn, what, errors, **kwargs):
    """עוטף קריאות boto3 ומחזיר None בשגיאה, תוך איסוף הודעות למסך."""
    try:
        return fn(**kwargs)
    except (ClientError, BotoCoreError) as e:
        errors.append(f"{what} failed: {str(e)}")
        return None

@app.route("/")
def home():
    errors = []

    # Instances
    instance_data = []
    reservations = _safe(ec2_client.describe_instances, "describe_instances", errors)
    for reservation in (reservations or {}).get("Reservations", []):
        for inst in reservation.get("Instances", []):
            instance_data.append({
                "ID": inst.get("InstanceId", "N/A"),
                "State": inst.get("State", {}).get("Name", "N/A"),
                "Type": inst.get("InstanceType", "N/A"),
                "Public IP": inst.get("PublicIpAddress", "—"),
            })

    # VPCs
    vpc_data = []
    vpcs_resp = _safe(ec2_client.describe_vpcs, "describe_vpcs", errors)
    for vpc in (vpcs_resp or {}).get("Vpcs", []):
        vpc_data.append({
            "VPC ID": vpc.get("VpcId", "N/A"),
            "CIDR": vpc.get("CidrBlock", "N/A"),
            "Default": str(vpc.get("IsDefault", False)),
        })

    # Load Balancers (handle pagination)
    lb_data = []
    marker = None
    while True:
        lbs_resp = _safe(
            elb_client.describe_load_balancers,
            "describe_load_balancers",
            errors,
            Marker=marker
        ) if marker else _safe(
            elb_client.describe_load_balancers,
            "describe_load_balancers",
            errors
        )
        if not lbs_resp:
            break
        for lb in lbs_resp.get("LoadBalancers", []):
            lb_data.append({
                "LB Name": lb.get("LoadBalancerName", "N/A"),
                "DNS Name": lb.get("DNSName", "N/A"),
                "Type": lb.get("Type", "N/A"),
                "Scheme": lb.get("Scheme", "N/A"),
            })
        marker = lbs_resp.get("NextMarker")
        if not marker:
            break

    # AMIs (owned by self) — נמיין לפי תאריך ונדגום עד 30 אחרונים להצגה
    ami_limit = 30
    ami_data = []
    images_resp = _safe(ec2_client.describe_images, "describe_images", errors, Owners=["self"])
    images = (images_resp or {}).get("Images", [])
    # חלק מה־AMIs אולי בלי CreationDate — נטפל בזה בעדינות
    def _cd(img): return img.get("CreationDate", "")
    images_sorted = sorted(images, key=_cd, reverse=True)[:ami_limit]
    for ami in images_sorted:
        ami_data.append({
            "AMI ID": ami.get("ImageId", "N/A"),
            "Name": ami.get("Name", "N/A"),
            "CreationDate": ami.get("CreationDate", "—"),
        })

    return render_template_string(
        HTML_TEMPLATE,
        region=REGION,
        instance_data=instance_data,
        vpc_data=vpc_data,
        lb_data=lb_data,
        ami_data=ami_data,
        ami_limit=ami_limit,
        errors=errors,
    )

if __name__ == "__main__":
    # חשוב ל־Docker: להאזין על כל האינטרפייסים ובפורט 5001
    app.run(host="0.0.0.0", port=5001)
