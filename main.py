from tkinter import *
import google.generativeai as ai

ai.configure(api_key="")
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}
model = ai.GenerativeModel(model_name="gemini-1.5-flash", generation_config=generation_config)

root = Tk()
root.title("DesktopAI")
root.geometry("1280x720")

class EntryWithPlaceholder(Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey'):
        super().__init__(master)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()

inputBox = EntryWithPlaceholder(root, placeholder="AI Input")
inputBox.grid(column=0, row=0, sticky="we")
root.grid_columnconfigure(0, weight=1)

aiResponse = Text(root, wrap="word", state="normal")
aiResponse.grid(column=0, row=1, sticky="nsew")
root.grid_rowconfigure(1, weight=1)

aiResponse.config(state="disabled")

# Set default font
aiResponse.tag_configure("normal", font=("Helvetica", 10))
aiResponse.tag_configure("bold", font=("Helvetica", 10, "bold"))
aiResponse.tag_configure("italic", font=("Helvetica", 10, "italic"))
aiResponse.tag_configure("code", font=("Courier", 10), background="lightgrey")

aiResponse.config(state="disabled")

chat_history = []

def insert_text(text):
    aiResponse.config(state='normal')
    aiResponse.delete('1.0', END)

    # Process text for formatting
    i = 0
    while i < len(text):
        if text[i:i+2] == '**':  # Check for bold
            end = text.find('**', i + 2)
            if end != -1:
                aiResponse.insert(END, text[i + 2:end], "bold")
                i = end + 2
            else:
                aiResponse.insert(END, text[i])
                i += 1
        elif text[i] == '*':  # Check for italic
            end = text.find('*', i + 1)
            if end != -1:
                aiResponse.insert(END, text[i + 1:end], "italic")
                i = end + 1
            else:
                aiResponse.insert(END, text[i])
                i += 1
        elif text[i:i+3] == '```':  # Check for code block
            end = text.find('```', i + 3)
            if end != -1:
                aiResponse.insert(END, text[i + 3:end], "code")
                i = end + 3
            else:
                aiResponse.insert(END, text[i])
                i += 1
        elif text[i] == '`':  # Check for inline code
            end = text.find('`', i + 1)
            if end != -1:
                aiResponse.insert(END, text[i + 1:end], "code")
                i = end + 1
            else:
                aiResponse.insert(END, text[i])
                i += 1
        else:
            aiResponse.insert(END, text[i], "normal")  # Regular text
            i += 1

    aiResponse.config(state='disabled')

def get_ai_response(event):
    user_input = inputBox.get()
    if user_input and user_input != "PLACEHOLDER":
        chat_history.append({"role": "user", "parts": [user_input] })
        chat = model.start_chat(history=chat_history)
        response = chat.send_message(user_input)
        chat_history.append({"role": "model", "parts": [response.text]})
        insert_text(response.text)
        inputBox.delete(0, END)

inputBox.bind("<Return>", get_ai_response)

root.mainloop()