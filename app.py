try:
  import unzip_requirements
except ImportError:
  pass

import os
from langchain import SelfAskWithSearchChain, SQLDatabaseChain, SQLDatabase, SerpAPIChain, LLMMathChain, OpenAI
from flask import Flask, request, jsonify
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

app = Flask(__name__)

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
SERP_API_KEY = os.environ.get('SERPAPI_API_KEY')
OPENAI_MODEL_NAME = os.environ['OPENAI_MODEL_NAME']

@app.route("/api/web_search", methods=['post'])
def api_web_search():
    try:
        body = request.get_json()

        input = body['input']
        uminal_user_id = body['user']['id']
        configuration = body['user']['configuration']

        # If a user has configured this app with their own API key, use that.
        # Otherwise, try to use ours (if it exists).
        api_key = configuration.get('api_key')
        if not api_key:
            if not SERP_API_KEY:
                return jsonify(success=False, error="Please provide an API key for SerpAPI."), 500
            api_key = SERP_API_KEY

        chain = SerpAPIChain(serpapi_api_key=api_key)

        output = chain.run(input)
        return jsonify(success=True, output=output)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify(success=False, error=f"Search failed: {e}"), 500


@app.route("/api/llm_math", methods=['post'])
def api_llm_math():
    try:
        body = request.get_json()

        input = body['input']
        uminal_user_id = body['user']['id']
        configuration = body['user']['configuration']

        # If a user has configured this app with their own API key, use that.
        # Otherwise, try to use ours (if it exists).
        api_key = configuration.get('api_key')
        if not api_key:
            if not OPENAI_API_KEY:
                return jsonify(success=False, error="Please provide an API key for OpenAI."), 500
            api_key = OPENAI_API_KEY

        chain = LLMMathChain(llm=OpenAI(
            openai_api_key=api_key, model_name=OPENAI_MODEL_NAME))

        output = chain.run(input)
        return jsonify(success=True, output=output)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify(success=False, error=f"Running the LLMMathChain failed: {e}"), 500


@app.route("/api/sql_db", methods=['post'])
def api_sql_db():
    try:
        body = request.get_json()

        input = body['input']
        uminal_user_id = body['user']['id']
        configuration = body['user']['configuration']

        # If a user has configured this app with their own API key, use that.
        # Otherwise, try to use ours (if it exists).
        api_key = configuration.get('api_key')
        if not api_key:
            if not OPENAI_API_KEY:
                return jsonify(success=False, error="Please provide an API key for OpenAI."), 500
            api_key = OPENAI_API_KEY

        db_uri = configuration['db_uri']

        db = SQLDatabase.from_uri(db_uri)
        chain = SQLDatabaseChain(
            llm=OpenAI(openai_api_key=api_key, model_name=OPENAI_MODEL_NAME),
            database=db
        )

        output = chain.run(input)
        return jsonify(success=True, output=output)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify(success=False, error=f"Querying the SQL DB failed: {e}"), 500
# if __name__ == "__main__":
#     app.run(debug=True, port=8080)