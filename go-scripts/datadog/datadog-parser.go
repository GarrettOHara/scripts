package main

import (
	"context"
	"encoding/json"
	"fmt"
	"os"
	"strconv"

	"github.com/DataDog/datadog-api-client-go/v2/api/datadog"
	"github.com/DataDog/datadog-api-client-go/v2/api/datadogV1"
)

func main() {

	CheckDatadogMonitor("10093143")

}

func CheckDatadogMonitor(MonitorOutput string) {
	fmt.Println("A")
	MonitorID, _ := strconv.ParseInt(MonitorOutput, 10, 64)
	ctx := datadog.NewDefaultContext(context.Background())
	configuration := datadog.NewConfiguration()
	apiClient := datadog.NewAPIClient(configuration)
	api := datadogV1.NewMonitorsApi(apiClient)
	
	fmt.Println("B")
	resp, r, err := api.GetMonitor(ctx, MonitorID, *datadogV1.NewGetMonitorOptionalParameters().WithWithDowntimes(true))
	
	fmt.Println("C")
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error when calling `MonitorsApi.GetMonitor`: %v\n", err)
		fmt.Fprintf(os.Stderr, "Full HTTP response: %v\n", r)
	}

	responseContent, _ := json.MarshalIndent(resp, "", "  ")
	fmt.Fprintf(os.Stdout, "Response from `MonitorsApi.GetMonitor`:\n%s\n", responseContent)
	
	fmt.Println("D")
	var response map[string]interface{}

	json.Unmarshal(responseContent, &response)
	
	fmt.Println("E")
	formatted_string := response["options"].(map[string]interface{})["thresholds"].(map[string]interface{})["critical"]
	fmt.Print(formatted_string)

}
