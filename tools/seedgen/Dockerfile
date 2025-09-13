FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src
COPY . ./
RUN dotnet publish seedgen.csproj -c Release -o /app/publish

FROM mcr.microsoft.com/dotnet/runtime:8.0 AS seed
WORKDIR /app
COPY --from=build /app/publish .
ENTRYPOINT ["dotnet","seedgen.dll"]
