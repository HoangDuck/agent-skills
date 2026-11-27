# Tracing

Use only the layers in scope. Walk **up** one level at a time, for every read and every write, until you reach a trigger a user or system can fire. Read the project profile for repo paths and local conventions; they override the defaults below.

## Statuses

| Status | Meaning |
|---|---|
| `LIVE` | chain reaches a nameable trigger (menu, route, button, job, webhook, public URL) |
| `DEAD` | code exists but the chain breaks; say where |
| `API_ONLY` | endpoint exists, no client found in the repos checked |
| `NO_ROUTE` | client calls a URL the backend does not have |
| `UNVERIFIED` | found but not opened, or the chain was not finished |

No nameable trigger means not `LIVE`. A similar name is not the same data: follow the URL to its backend handler.

## Any stack

- Backend: `route → handler → service → data model`, plus jobs and queues, signals or hooks, admin screens, import and sync code, raw queries, foreign keys.
- Client: `URL → API function → state or repository → view → whoever builds the view → menu, route, link or button`.
- Permissions come from the permission code itself, not from its name.

```bash
git grep -n -I --untracked -e "<url-path-or-symbol>" -- <source dirs>
git grep -n -I --untracked -w -e "<SymbolFromPreviousStep>" -- <source dirs>
# with --ref: git grep -n -I -e "<pattern>" <ref> -- <source dirs>
```

## Stack notes: "looks used" is `DEAD` unless…

### Django / DRF
- Check `include()` prefixes and router `register()` before naming a URL; `reverse()` and `{% url %}` use route **names**.
- Also: signals, management commands, Celery tasks and beat schedule, `admin.py`, ForeignKeys and `related_name` pointing at the model, serializer `source=` renames.

```bash
git grep -n -I --untracked -E "<app>|<Model>|<related_name>|<url-path>" -- . ':!<app>' ':!*/migrations/*'
git grep -n -E "<Model>\.objects\.|<Model>\(|<related_name>\.(create|add|set|update|delete|bulk_create)" -- . ':!*/migrations/*'
git grep -n -E "get_model\(|\.raw\(|connection\.cursor|<app>_<model>" -- . ':!*/migrations/*'
```

### Go (Echo, Gin, chi, net/http)
- A handler counts only if its route group is mounted from `main` (or the server setup) and middleware does not reject the caller.
- Interfaces are implicit: find implementations by method name, not by an `implements` keyword. DI (`wire`, `fx`) providers only register.
- Data: GORM models and `Table()` names, `sqlc` queries (search the query name in `.sql` and the generated method), raw SQL strings, JSON tags (`json:"field"`) as the wire name.

### PHP / Laravel
- `routes/*.php`, `Route::resource`, string handlers `'Controller@method'`; route names via `route('name')`.
- Events and listeners (`EventServiceProvider`), jobs, scheduler (`Console/Kernel` or `routes/console.php`), observers, policies and gates.
- Dynamic access (`$model->{$field}`, `$request->input($name)`) hides readers: search the string.

### Strapi
- Content types in `src/api/*/content-types/*/schema.json` (relations both ways), components, lifecycles, controller and service overrides, policies, middlewares.
- Auto REST routes `/api/<pluralName>` and `populate` params on clients. Role permissions live in the database (`seed` anchor).

### Flutter
| Pattern | `DEAD` unless |
|---|---|
| GetX controller in a binding | something calls `Get.find` or builds its `GetView` (`Get.lazyPut` only registers) |
| Bloc / Cubit | a `BlocProvider` sits above the reader and something adds the event or calls the method |
| Riverpod provider | something `watch`es or `read`s it |
| `get_it` / `injectable` | something resolves it (registration only registers) |
| Route (GetX, GoRouter, auto_route) | something navigates to it, and its binding or provider is set up |
| View renders the data | the page building it is referenced up to a menu, tab or route |
| Button exists | `Visibility`, cross-fade, permission check, `IgnorePointer`, `onPressed: null` or a comment does not block it |

Wire names: `@JsonKey(name:)`, `fromJson` keys; search source, not `.g.dart` / `.freezed.dart`.

### Next.js / React
| Pattern | `DEAD` unless |
|---|---|
| File under `pages/` or `app/` | it matches the routing rules (`pageExtensions`, `page.tsx`, route groups) or a route imports it |
| Shared screen | some route imports it |
| Page exists | a menu, link, `router.push`, redirect or public URL reaches it; a redirect away makes it unreachable |
| Control exists | auth wrappers, `middleware.ts`, permission hooks or a condition do not block it |

URLs are often template strings: search the stable prefix. Check `redirects` and `rewrites` in the framework config.

### iOS / SwiftUI
- Reachable through `NavigationLink`, `navigationDestination`, `sheet`, `fullScreenCover`, tab items or a coordinator.
- `@EnvironmentObject` must be injected above the reader. Wire names via `CodingKeys` and `keyDecodingStrategy`.

## Search hygiene

- An empty result counts only if the same pattern, without exclusions, finds the definition itself.
- Use `git grep -w`; `\b` can silently match nothing on macOS.
- Search every naming form the value travels under: `snake_case`, `camelCase`, the wire name, the label text.
- Search from the repo root; quote globs and pathspecs.
- Never cut result lists with `head` when counting readers or writers.
- A local default branch may lag the remote one: compare `git rev-parse <b> origin/<b>` and say which you read.
- Generated code (OpenAPI clients, codegen) points back to a source schema: trace the schema.
- Docs are claims. Code wins; report the mismatch.
