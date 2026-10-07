# cubecli org

Inspect your organization

## `cubecli org plan`

Show the organization's plan, renewal and scheduled changes

Show the commercial plan of the organization (Free, Pro, Business or
Enterprise): status, billing interval, price in USD, current period, renewal,
any change or cancellation scheduled for the end of the period, the monthly
plan credit and the plan invoices.

This command only reads the plan. Buy, change, cancel or resume it from the
Plan page of the dashboard: https://my.cubepath.com/organization/plan

Usage: `cubecli org plan`

Examples:

```
  cubecli org plan
  cubecli org plan --json
```
