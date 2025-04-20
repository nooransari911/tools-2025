# Merge existing code into a single file
python3 ./src/utils/merge-files-selected.py ./files/frontback.md ../AI_doc_processor_webapp/frontend/src/ ../AI_doc_processor_webapp/backend/app/schemas/api_models.py ../AI_doc_processor_webapp/backend/app/core/processor.py ../AI_doc_processor_webapp/backend/app/main.py


# Call AI on existing code
python3 ./gemini_generate\ new\ SDK\ copy.py -i ./files/ --schema StructuredFileListOutput pro paid ./prompt\ files/<prompt file> -o ./data/output_file_version.json


# Update all local code
python3 ./src/utils/deserialize.py <json-file containing AI model response> --base-dir ../AI_doc_processor_webapp/
