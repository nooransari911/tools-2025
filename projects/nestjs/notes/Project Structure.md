# app.service.ts
A basic service file with a single method.

It uses @Injectable from core. 











# app.controller.ts
This is a basic controller file containing a single route.

It uses app.service. Also @Controller and @Get/@Post/..... from core.









# app.controller.spec.ts
This file contains unit tests for the controller, adhering to the Nest.js focus on test-driven development (TDD)










# app.module.ts
This is the root module of the application, which imports other modules and providers. 



It uses app.controller and app.service. Also @Module from core










# main.ts
It serves as the entry point of your Nest.js application.


It uses app.module. It also uses Nest.js’s core function `NestFactory` to create an instance of your Nest application.













