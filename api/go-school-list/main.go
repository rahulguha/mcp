package main

import (
	"encoding/json"
	"fmt"
	"github.com/aws/aws-lambda-go/events"
	"github.com/aws/aws-lambda-go/lambda"
	"github.com/gorilla/mux"
	"io"
	"log"
	"net/http"
	"os"
)

// School represents a single school entry in the JSON
// URL represents a URL entry in the JSON
type URL struct {
	URL  string   `json:"url"`
	Tags []string `json:"tags"`
}

// School represents a single school entry in the JSON
type School struct {
	School string `json:"school"`
	URLs   []URL  `json:"urls"`
}
// loadSchools reads the JSON file and returns a slice of School
func loadSchools() ([]School, error) {
	file, err := os.Open("data/school_url.json")
	
	if err != nil {
		return nil, fmt.Errorf("failed to open school_list.json: %v", err)
	}
	defer file.Close()

	data, err := io.ReadAll(file)
	if err != nil {
		return nil, fmt.Errorf("failed to read school_url.json: %v", err)
	}
	var schools []School
	err = json.Unmarshal(data, &schools)
	if err != nil {
		return nil, fmt.Errorf("failed to unmarshal JSON: %v", err)
	}
	return schools, nil
}

// pingHandler responds with "ping"
func pingHandler(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK)
	fmt.Fprint(w, "ping")
}

// schoolsHandler returns the contents of school_list.json
func schoolsHandler(w http.ResponseWriter, r *http.Request) {
	schools, err := loadSchools()
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(schools)
}

// lambdaHandler adapts the API for AWS Lambda
func lambdaHandler(req events.APIGatewayProxyRequest) (events.APIGatewayProxyResponse, error) {
	switch req.HTTPMethod {
	case "GET":
		if req.Path == "/ping" {
			return events.APIGatewayProxyResponse{
				StatusCode: 200,
				Body:       "ping",
			}, nil
		} else if req.Path == "/schools" {
			schools, err := loadSchools()
			if err != nil {
				return events.APIGatewayProxyResponse{
					StatusCode: 500,
					Body:       err.Error(),
				}, nil
			}
			body, err := json.Marshal(schools)
			if err != nil {
				return events.APIGatewayProxyResponse{
					StatusCode: 500,
					Body:       "Failed to marshal JSON",
				}, nil
			}
			return events.APIGatewayProxyResponse{
				StatusCode: 200,
				Headers:    map[string]string{"Content-Type": "application/json"},
				Body:       string(body),
			}, nil
		}
	}
	return events.APIGatewayProxyResponse{
		StatusCode: 404,
		Body:       "Not Found",
	}, nil
}

// main sets up the HTTP server for local development
func main() {
	if os.Getenv("AWS_LAMBDA_FUNCTION_NAME") != "" {
		lambda.Start(lambdaHandler)
		return
	}

	r := mux.NewRouter()
	r.HandleFunc("/ping", pingHandler).Methods("GET")
	r.HandleFunc("/schools", schoolsHandler).Methods("GET")
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080" // Default port if not set by Cloud Run (for local testing)
	}
	log.Printf("Listening on port %s...", port)
	log.Fatal(http.ListenAndServe(fmt.Sprintf(":%s", port), r))
	// if err := http.ListenAndServe(":8080", r); err != nil {
	// 	log.Fatalf("Server failed: %v", err)
	// }
}