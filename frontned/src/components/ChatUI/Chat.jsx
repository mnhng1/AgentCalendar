import { useState } from 'react';
import UserContext from '../../context/UserContext'; 
import { useContext } from 'react';


const Chat = () => {
    const { user } = useContext(UserContext);
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (input.trim()) {
            setMessages([...messages, { text: input, sender: 'user' }]);
            try {
                const response = await fetch('http://localhost:8000/agent/execute/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${user?.access_token}`
                    },
                    body: JSON.stringify({
                        messages: messages.map(msg => ({
                            role: msg.sender === 'user' ? 'human' : 'assistant',
                            content: msg.text
                        })),
                        input: input
                    })
                });
                const data = await response.json();
                setMessages(prev => [...prev, { text: data, sender: 'assistant' }]);
            } catch (error) {
                console.error('Error:', error);
            }
            setInput('');
    };
    }

    return (
        <div className="flex flex-col h-[80vh] max-w-3xl mx-auto p-4 bg-white rounded-lg shadow-lg">
            {/* Chat messages */}
            <div className="flex-1 overflow-y-auto space-y-4 p-4">
                {messages.map((message, index) => (
                    <div 
                        key={index}
                        className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                        <div className={`max-w-[70%] rounded-lg p-3 ${
                            message.sender === 'user' 
                                ? 'bg-blue-500 text-white' 
                                : 'bg-gray-200 text-gray-800'
                        }`}>
                            {message.text}
                        </div>
                    </div>
                ))}
            </div>

            {/* Input form */}
            <form onSubmit={handleSubmit} className="flex gap-2 p-4 border-t">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    className="flex-1 p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Type a message..."
                />
                <button 
                    type="submit"
                    className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
                >
                    Send
                </button>
            </form>
        </div>
    );
};

export default Chat;