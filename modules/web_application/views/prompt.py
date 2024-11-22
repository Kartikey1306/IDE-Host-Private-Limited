from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from modules.web_application.models.prompt_log import PromptLog
from app import db
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

bp = Blueprint('prompt', __name__)

@bp.route('/generate-prompt', methods=['POST'])
@login_required
def generate_prompt():
    prompt_text = request.json['prompt']
    
    llm = OpenAI(temperature=0.9)
    prompt = PromptTemplate(
        input_variables=["question"],
        template="You are a helpful AI assistant. Answer the following question: {question}"
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    
    result = chain.run(question=prompt_text)
    
    prompt_log = PromptLog(
        prompt_text=prompt_text,
        generated_output=result,
        created_by_user_id=current_user.id
    )
    db.session.add(prompt_log)
    db.session.commit()
    
    return jsonify({
        'prompt': prompt_text,
        'response': result
    }), 201

@bp.route('/prompts', methods=['GET'])
@login_required
def get_prompts():
    prompts = PromptLog.query.filter_by(created_by_user_id=current_user.id).all()
    return jsonify([{
        'id': prompt.id,
        'prompt_text': prompt.prompt_text,
        'generated_output': prompt.generated_output,
        'created_at': prompt.created_at
    } for prompt in prompts])

@bp.route('/prompts/<int:id>', methods=['DELETE'])
@login_required
def delete_prompt(id):
    prompt = PromptLog.query.get_or_404(id)
    if prompt.created_by_user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    db.session.delete(prompt)
    db.session.commit()
    return '', 204

