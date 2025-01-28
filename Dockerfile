# First stage: Build the native image
FROM ghcr.io/graalvm/native-image-community:21 AS build


# Set the working directory
WORKDIR /usr/src/app

# Copy Maven configuration and download dependencies
COPY pom.xml .
COPY mvnw .
COPY .mvn ./.mvn
RUN ./mvnw dependency:go-offline

# Copy the application source code
COPY src/main ./src/main

# Compile the native image, skipping tests for faster build
RUN ./mvnw -Pnative native:compile -DskipTests

# Second stage: Create a lightweight image to run the application
FROM alpine:latest AS final-stage

# Set the working directory
WORKDIR /app

# Copy the native binary from the build stage
COPY --from=build /usr/src/app/target/ska-src-mm-image-discovery /app/ska-src-mm-image-discovery

# Install required libraries for running the native image
RUN apk add --no-cache libstdc++ libc6-compat


# Expose the port for the application
EXPOSE 8080

# Run the application
ENTRYPOINT ["/app/ska-src-mm-image-discovery"]
