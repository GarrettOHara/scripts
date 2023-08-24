package main

import (
	"encoding/json"
	"fmt"
)

func main() {
	jsonData := `{
	  "created": "2019-06-07T14:40:06.863Z",
	  "created_at": 1559918406000,
	  "creator": {
	    "email": "scott.trenda@sportngin.com",
	    "handle": "scott.trenda@sportngin.com",
	    "id": 1289070,
	    "name": "Scott Trenda"
	  },
	  "deleted": null,
	  "id": 10093143,
	  "matching_downtimes": [],
	  "message": "The Travis build time is {{value}} seconds.\n\n{{#is_alert}}See what's taking so much time, this is a little ridiculous.{{/is_alert}}\n{{#is_warning}}Take a look at the build time on sport_admin.{{/is_warning}}\n\n{{#is_recovery}}Build time is back to normal levels.{{/is_recovery}}\n\nNotify:, More information: [Ops Guide](http://ops.myorg.com/guide) @scott.trenda@sportngin.com",
	  "modified": "2019-06-07T14:42:30.886Z",
	  "multi": false,
	  "name": "sport_admin Travis build time",
	  "options": {
	    "escalation_message": "",
	    "include_tags": true,
	    "locked": false,
	    "new_host_delay": 300,
	    "no_data_timeframe": null,
	    "notify_audit": false,
	    "notify_no_data": false,
	    "renotify_interval": 0,
	    "require_full_window": true,
	    "silenced": {},
	    "thresholds": {
	      "critical": 1200,
	      "warning": 900
	    },
	    "timeout_h": 0
	  },
	  "org_id": 125181,
	  "overall_state": "Alert",
	  "overall_state_modified": "2022-08-16T19:26:04+00:00",
	  "priority": null,
	  "query": "avg(last_1h):avg:travis_ci.build.duration{repo_name:sportngin/sport_admin,!event_type:pull_request} \u003e 1200",
	  "restricted_roles": null,
	  "tags": [],
	  "type": "metric alert"
	}`

	var data map[string]interface{}

	err := json.Unmarshal([]byte(jsonData), &data)
	if err != nil {
		fmt.Println("Error:", err)
		return
	}

//	fmt.Println("Alert Name:", data["name"])
//	fmt.Println("Creator Name:", data["creator"].(map[string]interface{})["name"])
//	fmt.Println("Message:", data["message"])
	
	fmt.Print("Critical Threshold: ")
	formattedString := data["options"].(map[string]interface{})["thresholds"].(map[string]interface{})["critical"]
	fmt.Println(formattedString)
}
