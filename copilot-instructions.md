# Project Overview

This project is a web application with backend services (microservices) that allows users to plan trips. The user can ask in natural langauge, for example "Plan a trip next week to a warm and sunny location, a maximum of around two hours flying time from London, somewhere with nice beaches and good food". The application will make use of a large language model to generate a trip plan, including flights, accommodation, and activities, whilst performing checks to ensure the plan meets the users requirements, such as checking historical weather data or even current forecasts, and ensuring the flights are within the specified time limit and so on.

## Folder Structure

## Libraries and Frameworks

Frontend: Next.js
Core services: Python FastAPI
CLI Apps: C# .NET 9

## Coding Standards

## UI Guidelines

The UI should be clean and simple, with a focus on usability. The design should be responsive and work well on both desktop and mobile devices. Use a consistent color scheme and typography throughout the application. A chat interface should be used to allow the user to interact with the application in a natural way, with a separate section to display the generated trip plan as it is created in real-time.

## Additional Objectives

This application will in part be used to test and demonstrate the use of various tools in a DevSecOps pipeline to ensure that the code is secure and compliant with best practices. This will include tools for static code analysis, dependency checking, container security, and infrastructure as code (IaC) scanning. You should intentionally introduce some security vulnerabilities and compliance issues into the codebase to demonstrate the effectiveness of these tools.
