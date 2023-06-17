# Reddit Feed

### Description
Reddit Feed

### Quickstart
##### Clone the repository with the PR branch (feature/app-base) and navigate to it:
```console
git clone -b feature/app-base git@github.com:quantumwaffy/reddit_feed.git && cd $(basename $_ .git)
```
##### Run project:
```console
make up
```
##### [Open the service Swagger in browser](http://0.0.0.0:8000/docs)

##### Shutdown and purge:
```console
make rmi
```

### Future improvements
1. **Authentication**
   - add a `User` model to collect feed users
   - add a `UserSettings` model with a _OneToOne_ relationship to the `User` model to collect private settings 
     and preferences
   - implement authentication with _JWT-tokens_
     - add secret keys for generating _access_ and _refresh_ tokens to `Settings` as environment variables
     - add endpoints to create new account, sign in and sign out
     - add _FastAPI_ dependency as a variable using `Annotated` to verify user authentication for endpoints
2. **Meta-information block for the feed page in the response**
   - add the `page` attribute to display the current page number in the response
   - add the `total` attribute to display the total number of records
   - add the `size` attribute to display the page size
   - add the `pages` attribute to display the total number of records
   - add _Cursor-based pagination_ for the feed to make it adaptable to _Infinite Scrolling_ for the _FrontEnd_
3. **Feed building**
   - with the addition of users and settings for them, need to add a pre-filtering by `subreddit` 
     from the preference (_subscriptions_) of a particular user
4. **Database Indexes**
    - index field `promoted` to speed up the selection of promoted posts
    - index field `subreddit_id` to speed up the selection by `Subreddit` for a particular user
5. **CRUD**
    - implement _Read_, _Update_ and _Delete_ for `Post` and `Subreddit` models (for the current task is 
      implemented only *Create*)
