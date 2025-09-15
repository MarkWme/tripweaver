FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
ARG ARTIFACTORY_NUGET_SOURCE
ARG ARTIFACTORY_NUGET_USERNAME
ARG ARTIFACTORY_NUGET_PASSWORD
WORKDIR /src
COPY . ./
# If Artifactory NuGet source details provided, add it transiently
RUN set -e; \
	 if [ -n "$ARTIFACTORY_NUGET_SOURCE" ]; then \
		 echo "Configuring Artifactory NuGet source: $ARTIFACTORY_NUGET_SOURCE"; \
		 if [ -n "$ARTIFACTORY_NUGET_USERNAME" ] && [ -n "$ARTIFACTORY_NUGET_PASSWORD" ]; then \
			 dotnet nuget add source "$ARTIFACTORY_NUGET_SOURCE" --name Artifactory --username "$ARTIFACTORY_NUGET_USERNAME" --password "$ARTIFACTORY_NUGET_PASSWORD" --store-password-in-clear-text; \
		 else \
			 dotnet nuget add source "$ARTIFACTORY_NUGET_SOURCE" --name Artifactory; \
		 fi; \
	 fi; \
	 dotnet restore seedgen.csproj; \
	 dotnet publish seedgen.csproj -c Release -o /app/publish; \
	 dotnet nuget remove source Artifactory || true

FROM mcr.microsoft.com/dotnet/runtime:8.0 AS seed
WORKDIR /app
COPY --from=build /app/publish .
ENTRYPOINT ["dotnet","seedgen.dll"]
