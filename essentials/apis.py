from openai import OpenAI
from groq import Groq
from .xero import blockize,Compiler,BlockChain
from markdown_it import MarkdownIt
from together import Together
from together.types import chat_completions 

class ChatGPT_API:
    model="gpt-3.5-turbo"
    max_tokens=8000
    def __init__(self,apikey):
        self.client = OpenAI(api_key=apikey)
        self.messages = []
        self.compiler = Compiler(BlockChain("_STARTER_BLOCKCHAIN"))
    def demo_speech(self,text):
        out= self.client.audio.speech.create(text, "tts-1","fable",) # voices:Literal['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer']
        return out
    def get_formatted_messages(self):
        self.convert_message_roles()
        fmessages=[]
        copymessages = self.messages.copy()
        for msg in copymessages:
            newmsg = msg.copy()
            if newmsg['role'] == 'assistant':
                content = ""
                for chunk in self.compiler.update_blockchain(blockize(newmsg['content'])).execute():
                    content+=chunk
                MI =MarkdownIt('commonmark',{'html':True,'breaks':True})
                
                newmsg['content'] = MI.render(content) #.replace("\n",'<br>')
            fmessages.append(newmsg)
        self.convert_message_roles()
        return fmessages
    def chat_pure_message(self,role,content):
        comp=self.client.chat.completions.create(
        messages=[
            {
                "role": role,
                "content": content,
        }],
        max_tokens=ChatGPT_API.max_tokens,
        model=ChatGPT_API.model)
        return comp
    def user_message(self,content):
        self.messages.append({"role":"user","content":content})
        comp = self.client.chat.completions.create(messages=self.messages,model=ChatGPT_API.model,max_tokens=ChatGPT_API.max_tokens)
        self.messages.append({"role":comp.choices[0].message.role,"content":comp.choices[0].message.content})
        return comp
    def system_message(self,content,execute=True):
        self.messages.append({"role":"system","content":content})
        self.messages.append({"role":"assistant","content":"$SEND_MESSAGE Start\nHello👋 I am Genos, your virtual assistant. I can do simple tasks on your system if you want...\nI am made using an ULTRAX model of OMEGAPy-XERO Project.\nLet's chat for a bit...\n$END_BLOCK Start"})
    def convert_message_roles(self):
        return True

class Groq_API:
    model = "llama3-8b-8192" #"llama3-70b-8192"
    max_tokens=8000
    def __init__(self,apikey):
        self.client = Groq(api_key=apikey)
        self.messages = []
        self.compiler = Compiler(BlockChain("_STARTER_BLOCKCHAIN"))
    def get_formatted_messages(self):
        self.convert_message_roles()
        fmessages=[]
        copymessages = self.messages.copy()
        for msg in copymessages:
            newmsg = msg.copy()
            if newmsg['role'] == 'assistant':
                content = ""
                for chunk in self.compiler.update_blockchain(blockize(newmsg['content'])).execute():
                    content+=chunk
                MI =MarkdownIt('commonmark',{'html':True,'breaks':True})
                
                newmsg['content'] = MI.render(content) #.replace("\n",'<br>')
            fmessages.append(newmsg)
        self.convert_message_roles()
        return fmessages
    def chat_pure_message(self,role,content):
        comp=self.client.chat.completions.create(
        messages=[
            {
                "role": role,
                "content": content,
        }],
        max_tokens=Groq_API.max_tokens,
        model=Groq_API.model)
        return comp
    def user_message(self,content):
        self.messages.append({"role":"user","content":content})
        comp = self.client.chat.completions.create(messages=self.messages,model=Groq_API.model,max_tokens=Groq_API.max_tokens)
        self.messages.append({"role":comp.choices[0].message.role,"content":comp.choices[0].message.content})
        return comp
    def system_message(self,content,execute=True):
        self.messages.append({"role":"system","content":content})
        self.messages.append({"role":"assistant","content":"$SEND_MESSAGE Start\nHello👋 I am Genos, your virtual assistant. I can do simple tasks on your system if you want...\nI am made using an ULTRAX model of OMEGAPy-XERO Project.\nLet's chat for a bit...\n$END_BLOCK Start"})
    def convert_message_roles(self):
        return True

class TogetherAI:
    model = "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo"
    max_tokens = 8000
    def __init__(self,apikey):
        self.client = Together(api_key=apikey)
        self.messages = []
        self.compiler = Compiler(BlockChain("_STARTER_BLOCKCHAIN"))
    def get_formatted_messages(self):
        self.convert_message_roles()
        fmessages=[]
        copymessages = self.messages.copy()
        for msg in copymessages:
            newmsg = msg.copy()
            if newmsg['role'] == 'assistant':
                content = ""
                for chunk in self.compiler.update_blockchain(blockize(newmsg['content'])).execute():
                    content+=chunk
                MI =MarkdownIt('commonmark',{'html':True,'breaks':True})
                
                newmsg['content'] = MI.render(content) #.replace("\n",'<br>')
            fmessages.append(newmsg)
        self.convert_message_roles()
        return fmessages
    def chat_pure_message(self,role,content):
        comp=self.client.chat.completions.create(
        messages=[
            {
                "role": role,
                "content": content,
        }],
        max_tokens=TogetherAI.max_tokens,
        model=TogetherAI.model)
        return comp
    def user_message(self,content):
        self.messages.append({"role":"user","content":content})
        comp = self.client.chat.completions.create(messages=self.messages,model=TogetherAI.model,max_tokens=TogetherAI.max_tokens)
        self.messages.append({"role":comp.choices[0].message.role,"content":comp.choices[0].message.content})
        self.convert_message_roles()
        return comp
    def system_message(self,content,execute=True):
        self.messages.append({"role":"system","content":content})
        self.messages.append({"role":"assistant","content":"$SEND_MESSAGE Start\nHello👋 I am Genos, your virtual assistant. I can do simple tasks on your system if you want...\nI am made using an ULTRAX model of OMEGAPy-XERO Project.\nLet's chat for a bit...\n$END_BLOCK Start"})
    def convert_message_roles(self):
        for i in range(len(self.messages)):
            if self.messages[i]['role'] == chat_completions.MessageRole.ASSISTANT and str(self.messages[i]['role']) != self.messages[i]['role']:
                self.messages[i]['role'] = 'assistant'
        return True

select_api = {
    "chatgpt" : ChatGPT_API,
    "groq" : Groq_API,
    "together" : TogetherAI
}