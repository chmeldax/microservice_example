# Example of microservice

This is an example project implementing small data-pulling microservice. The project is based on the
assignment by **PrismFP**.

## Requirements

 * PostgreSQL (including dev packages)
 * Redis
 * Python 3

 Also, optionally:
 * Nagios
 * Riemann

## Building

```bash
make clean && make
```

## Running

Firstly supply configuration file `config/config.yaml` based on the `config/config.yaml.example`. It should be pretty straightforward.

```bash
make run
```

## Deploying

```bash
make deploy
```

## Testing

```bash
make test
```

## Requesting the app

Just `POST` this with `application/json` Content-Type.

```javascript
{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "get_users",
    "params": []
}
```

## Remarks about the assignment

### General remarks

The service is based on the *JSON-RPC 2.0* standard over HTTP. We could easily think about other solutions with
better performance, for instance communicating directly via sockets and protobuffs. This can lead to significant
performance gain, but sometimes (from the developer's perspective) it can be a huge overkill.

Database table is defined without any secondary index, because it seems the table will be used just for obtaining
all users, so it would just lower the performance (when doing upserts).

We can have a flame war about using Factory & DI patterns vs Service Locator (used in this project), I just felt
that the latter one is more pythonic.


### Tests

If you have a look at my test helper, you can see I strongly favour integration (and similar) tests.
There are several reason why I believe *pure* (i.e. mocks everywhere) unit tests can be detrimental:

* It can make refactoring unbelievably hard.
* It does not provide enough confidence our code really works.

If we take that database helper as an example, I believe mocking the DB will either test nothing (we are testing
against our mock that is probably not the precise copy of the DB) or we end up with reimplementing our own RDBMS. That's
why I believe testing against real database instance (although with test data) is the right way.

The same applies to other 3rd party services (like Sentry, Riemann, etc.). It believe mocking these give us no gain.

But, this does not mean we cannot use TDD. No, the other way round. It seems to me that TDD can be used (and was used)
very easily when not having to worry about implementing any stubs/mocks.

### Deployment


I would prefer to use Capistrano from the Ruby world, but then I decided to implement something more pythonic.
But you can probably see that my solution is still heavily inspired by Capistrano (releases folder, symlink current, way of
implementing hooks etc.)

There are several way how to enhance this script:
* Introduce pruning of the old releases (I just wanted to be agile, you know :o)
* Use ssh-agent (*paramiko* library seems to have problems with it)
* Use `git pull` instead of `rsync`
* Store whole script somewhere else....

But definitely, there are a lot more approaches than just this one. I can think of introducing whole boxes provisioned
by Docker, orchestrated for example by Kubernetes etc. Also, making installable packages with some build server
(like Jenkins) can be a way to go. I am curious about your favourite way of doing things, guys :).

Just one remark about provisioning. The solution with introducing separate config file and deploying it with
the codebase is a bit ugly. I would prefer provisioning it by Puppet and/or implementing somekind of service discovery
solution (like Consul). But well, I hope my solution is good enough.


### Monitoring

This is the tricky part, because I know **nothing** about your infrastructure. So, I took two approaches:

* Creating pinging script (that also checks for valid responses) that can be used as a Nagios plugin. We could find
a lot of more thing to monitor, but I think it would be crazy to implement whole monitoring stack just because
of this one particular microservice. Let me know if you want me to show some more inputs. Look at `misc/nagios` folder.
* Monitoring application from within (pushing notifications to Riemann) and then acting on it. Currently the service
is so simple I can't think about any good metrics to track, so I just implemented looking for expired events.

### Thoughts?

If you need more input from me, please do contact me :).
