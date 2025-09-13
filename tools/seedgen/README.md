Seed generator (C# .NET 8)

This CLI reads data/destinations.csv and emits data/index.json for fast consumption by the API.

Build & run:

cd tools/seedgen
dotnet build -c Release
dotnet run --project .

Or via Docker (recommended for Makefile):
docker build --target seed -t tripweaver-seedgen:local .
docker run --rm -v $(pwd)/../../data:/app/data tripweaver-seedgen:local
