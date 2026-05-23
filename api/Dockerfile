FROM maven:3.9.9-eclipse-temurin-21-jammy as build

WORKDIR /app

COPY pom.xml ./pom.xml

RUN mvn dependency:tree

COPY . .

RUN mvn package

FROM eclipse-temurin:17.0.19_10-jdk-jammy

COPY --from=build /app/target/*.jar app.jar

EXPOSE 8080

CMD ["java", "-jar", "app.jar"]