# Listeners

## Hard Delete

- Listen for `onCreate` of `Conversations` container
    - Extract `cache_key`, `timestamp`, and perhaps other fields: `customerID`, etc.
    - Create new document within `Questions` container
- Listen for `onCreate` of `Questions` container
    - Extract `cache_key`
    - Find document in `TopQuestions` with `cache_key` value matching (every document will have a DISTINCT `cache_key` value)
    - Increment counter `counter++`
- Establish Document life-cycle policy on `Questions` collection
    - Managed by CosmosDB Document TTL
        - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/time-to-live
    - Once documents are outside of window, `DELETE` the document from this collection
- Listen from `onDelete` of `Questions` container
    - Extract `cache_key` value
    - Find document in `TopQuestions` with `cache_key` value matching (every document will have a DISTINCT `cache_key` value)
    - Decrement counter `counter--`

---

# Listeners

## Soft Delete / Expire

- Listen for `onCreate` of `Conversations` container
    - Extract `cache_key` value
    - Find document in `TopQuestions` with `cache_key` value matching (every document will have a DISTINCT `cache_key` value)
    - Increment counter `counter++`
- Life-cycle policy
    - We will need to create some manual life-cycle job to "soft delete" or "expire"
        - Runs every `n` minute/hour/day?
        - Runs `onEvent`: create?
    - Whatever job we go with, this will find documents/questions that have expired (7 day window)
    - Update field of document in `Conversations` container: `expired: true`
- Listen for `onUpdate` of Conversations container
    - If `expired: true`
    - Extract `cache_key` value
    - Find document in `TopQuestions` with `cache_key` value matching (every document will have a DISTINCT `cache_key` value)
    - Decrement counter `counter--`
