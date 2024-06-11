import google.generativeai as genai
import DocumentReader

# Takes the file path as the input.
print("Provide the path of the file: ")
path = input()

# Distinguishes the format of the file using the path.
# The correct text extractor will be used as per the format.
idx = path.rindex('.')
file_format = path[idx+1:]
prob = ""
if file_format == "pdf":
    prob = DocumentReader.pdfTextExtractor(path)
elif file_format == "xlsx":
    prob = DocumentReader.xlxsExtractor(path)
elif file_format == "docx":
    prob = DocumentReader.wordExtractor(path)
elif file_format == "csv":
    prob = DocumentReader.csvExtractor(path)

# Initializing the model.

GOOGLE_API_KEY = "xxx-xx-xxxx"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(
    'gemini-1.5-flash-latest',
    system_instruction="You are a python code generator. Generate python code required to accomplish the task.\
                       Return the python code."
)

# Takes the task to be completed as input
print("The task to be completed: ")
user_prompt = input()

# Generates response using Gemini API
response = model.generate_content(user_prompt + str(prob))
code = response.text
print(code)

# Code Execute Module
# The generated code is passed through exec to get an output.
python_code = code.splitlines()
python_code = "\n".join(python_code[1:-1])
exec(python_code)

# Integration with Vanilla LLM
# The code is passed to the LLM for running.
response = model.generate_content("Provide the output of the following code: " + code)
print(response.text)
