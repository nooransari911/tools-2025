# Controllers
Controllers in Nest.js form API endpoints: handling request and sending response. It acts as a gateway between client and core business logic on server. Any request is routed to the correct route in the correct controller.

# Creating new controllers
`@Controller ()` decorator defines a new controller. It can optionally accept a route path prefix. This is how controllers are used to group similar/related routes.

`@Get ()` decorator defines the HTTP request method. It can optionally accept path.

The HTTP request method and the paths as defined in the controller and HTTP request decorators form the API endpoint. An example endpoint is `GET /cats/breeds/` for `@Controller ('cats')` and `@Get ('breeeds')`.


# Returning from controllers
THe route method can directly return a JS object or any primitive (string, number, boolena, etc.). Nest automatically serializes JS object into JSON.

HTTP status code can optionally be defined with `@HttpCode ()`. By default, it is automatically set to 200 for GET and 201 for POST.



# Request object
Nest provides access to the request object of the underlying platform (Express by default). We can access the request object by instructing Nest to inject it by adding the `@Req()` decorator to the handler's signature.

The request object represents the HTTP request and has properties for the request query string, parameters, HTTP headers, body and more. In most cases, it's not necessary to grab these properties manually. We can use dedicated decorators instead, such as `@Body()` or `@Query()`, which are available out of the box.

Below is a list of the provided decorators and the plain platform-specific objects they represent.

@Request(), @Req()	                    req
@Response(), @Res()*	                res
@Next()	                                next
@Session()	                            req.session
@Param(key?: string)	                req.params / req.params[key]
@Body(key?: string)	                    req.body / req.body[key]
@Query(key?: string)	                req.query / req.query[key]
@Headers(name?: string)	                req.headers / req.headers[name]
@Ip()	                                req.ip
@HostParam()	                        req.hosts




# Resources

Earlier, we defined an endpoint to fetch the cats resource (GET route). We'll typically also want to provide an endpoint that creates new records.


It's that simple. Nest provides decorators for all of the standard HTTP methods: @Get(), @Post(), @Put(), @Delete(), @Patch(), @Options(), and @Head(). In addition, @All() defines an endpoint that handles all of them.



# Using services
Do:

```
@Controller ("auth")
export class AuthController () {
 constructor (private authservice: AuthService) {}

 @Get ("route") {
  return this.authservice.function ();
 }
}



```









# Route Wildcards
Pattern-based routes are also supported in NestJS.

For example, the asterisk (*) can be used as a wildcard to match any combination of characters in a route at the end of a path. Thus, `@Get ('abcd/*')` will be executed regardless of what follow abcd/.

@Get('abcd/*')


# Status code

As mentioned, the response status code is always 200 by default, except for POST requests which are 201. We can easily change this behavior by adding the `@HttpCode(...)` decorator at a handler level.


Often, your status code isn't static but depends on various factors. In that case, you can use a library-specific response (inject using @Res()) object (or, in case of an error, throw an exception).



@Post()
@HttpCode(204)




# Headers

To specify a custom response header, you can either use a @Header() decorator or a library-specific response object (and call res.header() directly).


@Post()
@Header('Cache-Control', 'no-store')




# Redirection

To redirect a response to a specific URL, you can either use a @Redirect() decorator or a library-specific response object (and call res.redirect() directly).

@Redirect() takes two arguments, url and statusCode, both are optional. The default value of statusCode is 302 (Found) if omitted.

Sometimes you may want to determine the HTTP status code or the redirect URL dynamically. Do this by returning an object following the HttpRedirectResponse interface (from @nestjs/common).



@Get()
@Redirect('https://nestjs.com', 301)






# Route parameters

Routes with static paths won't work when you need to accept dynamic data as part of the request (e.g., GET /cats/1 to get cat with id 1). In order to define routes with parameters, we can add route parameter tokens in the path of the route to capture the dynamic value at that position in the request URL. Route parameters declared in this way can be accessed using the @Param() decorator, which should be added to the method signature.

@Param() is used to decorate a method parameter (params in the example above), and makes the route parameters available as properties of that decorated method parameter inside the body of the method. As seen in the code below, we can access the id parameter by referencing params.id. 

@Get('cats/:id')
finaAll (@Param () params: string): string {
    console.log (params.id);
    return "hello";
}





You can also pass in a particular parameter token to the decorator, and then reference the route parameter directly by name in the method body.


@Get('cats/:id')
finaAll (@Param ('id') id: string): string {
    console.log (id);
    return "hello";
}



Routes with parameters should be declared after any static paths. This prevents the parameterized paths from intercepting traffic destined for the static paths. 










# Sub-Domain Routing

The @Controller decorator can take a host option to require that the HTTP host of the incoming requests matches some specific value.

@Controller({ host: 'admin.example.com' })




Similar to a route path, the hosts option can use tokens to capture the dynamic value at that position in the host name. The host parameter token in the @Controller() decorator example below demonstrates this usage. Host parameters declared in this way can be accessed using the @HostParam() decorator, which should be added to the method signature.


@Controller({ host: ':account.example.com' })
export class AccountController {
  @Get()
  getInfo(@HostParam('account') account: string) {
    return account;
  }
}





# Scopes

For people coming from different programming language backgrounds, it might be unexpected to learn that in Nest, almost everything is shared across incoming requests. We have a connection pool to the database, singleton services with global state, etc. Remember that Node.js doesn't follow the request/response Multi-Threaded Stateless Model in which every request is processed by a separate thread. Hence, using singleton instances is fully safe for our applications.

However, there are edge-cases when request-based lifetime of the controller may be the desired behavior, for instance per-request caching in GraphQL applications, request tracking or multi-tenancy.




# Asynchronicity

We love modern JavaScript and we know that data extraction is mostly asynchronous. That's why Nest supports and works well with async functions.


Every async function has to return a Promise. This means that you can return a deferred value that Nest will be able to resolve by itself. Let's see an example of this:

@Get()
async findAll(): Promise<any[]> {
  return [];
}

The above code is fully valid.




Furthermore, Nest route handlers are even more powerful by being able to return RxJS observable streams. Nest will automatically subscribe to the source underneath and take the last emitted value (once the stream is completed).


@Get()
findAll(): Observable<any[]> {
  return of([]);
}

Both of the above approaches work and you can use whatever fits your requirements.




# Request payloads

Our previous example of the POST route handler didn't accept any client params. Let's fix this by adding the @Body() decorator here.

But first (if you use TypeScript), we need to determine the DTO (Data Transfer Object) schema. A DTO is an object that defines how the data will be sent over the network. We could determine the DTO schema by using TypeScript interfaces, or by simple classes.


Interestingly, we recommend using classes here. Why? Classes are part of the JavaScript ES6 standard, and therefore they are preserved as real entities in the compiled JavaScript. On the other hand, since TypeScript interfaces are removed during the transpilation, Nest can't refer to them at runtime. This is important because features such as Pipes enable additional possibilities when they have access to the metatype of the variable at runtime.





Let's create the CreateCatDto class:



export class CreateCatDto {
  name: string;
  age: number;
  breed: string;
}

It has only three basic properties. Thereafter we can use the newly created DTO inside the CatsController:


@Post()
async create(@Body() createCatDto: CreateCatDto) {
  return 'This action adds a new cat';
}

Our ValidationPipe can filter out properties that should not be received by the method handler. In this case, we can whitelist the acceptable properties, and any property not included in the whitelist is automatically stripped from the resulting object. In the CreateCatDto example, our whitelist is the name, age, and breed properties. Learn more here. 









# Full resource sample

Below is an example that makes use of several of the available decorators to create a basic controller. This controller exposes a couple of methods to access and manipulate internal data.


cats.controller.ts

```
import { Controller, Get, Query, Post, Body, Put, Param, Delete } from '@nestjs/common';
import { CreateCatDto, UpdateCatDto, ListAllEntities } from './dto';

@Controller('cats')
export class CatsController {
  @Post()
  create(@Body() createCatDto: CreateCatDto) {
    return 'This action adds a new cat';
  }

  @Get()
  findAll(@Query() query: ListAllEntities) {
    return `This action returns all cats (limit: ${query.limit} items)`;
  }

  @Get(':id')
  findOne(@Param('id') id: string) {




#     return `This action returns a ${id} cat`;
  }

  @Put(':id')
  update(@Param('id') id: string, @Body() updateCatDto: UpdateCatDto) {




#     return `This action updates a ${id} cat`;
  }

  @Delete(':id')
  remove(@Param('id') id: string) {




#     return `This action removes a ${id} cat`;
  }
}
```



Nest CLI provides a generator (schematic) that automatically generates all the boilerplate code to help us avoid doing all of this, and make the developer experience much simpler. Read more about this feature here. 





# Getting up and running

With the above controller fully defined, Nest still doesn't know that CatsController exists and as a result won't create an instance of this class.

Controllers always belong to a module, which is why we include the controllers array within the @Module() decorator. Since we haven't yet defined any other modules except the root AppModule, we'll use that to introduce the CatsController:
app.module.ts
JS


import { Module } from '@nestjs/common';
import { CatsController } from './cats/cats.controller';

@Module({
  controllers: [CatsController],
})
export class AppModule {}

We attached the metadata to the module class using the @Module() decorator, and Nest can now easily reflect which controllers have to be mounted.




# Library-specific approach

So far we've discussed the Nest standard way of manipulating responses. The second way of manipulating the response is to use a library-specific response object. In order to inject a particular response object, we need to use the @Res() decorator. To show the differences, let's rewrite the CatsController to the following:
JS


import { Controller, Get, Post, Res, HttpStatus } from '@nestjs/common';
import { Response } from 'express';

@Controller('cats')
export class CatsController {
  @Post()
  create(@Res() res: Response) {
    res.status(HttpStatus.CREATED).send();
  }

  @Get()
  findAll(@Res() res: Response) {
     res.status(HttpStatus.OK).json([]);
  }
}

Though this approach works, and does in fact allow for more flexibility in some ways by providing full control of the response object (headers manipulation, library-specific features, and so on), it should be used with care. In general, the approach is much less clear and does have some disadvantages. The main disadvantage is that your code becomes platform-dependent (as underlying libraries may have different APIs on the response object), and harder to test (you'll have to mock the response object, etc.).

Also, in the example above, you lose compatibility with Nest features that depend on Nest standard response handling, such as Interceptors and @HttpCode() / @Header() decorators. To fix this, you can set the passthrough option to true, as follows:
JS


@Get()
findAll(@Res({ passthrough: true }) res: Response) {
  res.status(HttpStatus.OK);
  return [];
}

Now you can interact with the native response object (for example, set cookies or headers depending on certain conditions), but leave the rest to the framework.




