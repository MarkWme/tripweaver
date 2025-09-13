Helm chart for TripWeaver

This chart contains basic Deployment and Service templates to run the API component. Values are intentionally minimal for local testing.

Install locally (example):

helm template charts/tripweaver | kubectl apply -f -
