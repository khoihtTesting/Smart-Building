import azure.functions as func
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="azure_trigger")
@app.blob_output(
    arg_name="outputblob", 
    path="samples-output/{rand-guid}.txt", 
    connection="AzureWebJobsStorage"
)
def azure_trigger(req: func.HttpRequest, outputblob: func.Out[str]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    # Nội dung bạn muốn lưu vào Blob Storage
    content_to_save = f"Hello, {name}! This data was saved from Azure Function via output binding." if name else "Hello, Anonymous! Default content saved."

    # Gán nội dung vào biến binding đầu ra để lưu file tự động lên Blob Storage
    outputblob.set(content_to_save)

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully and saved a blob.")
    else:
        return func.HttpResponse(
            "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body to customize the saved blob.",
            status_code=200
        )