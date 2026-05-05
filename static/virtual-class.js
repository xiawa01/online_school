// Virtual Class на чистом JS + LiveKit
class VirtualClass {
    constructor(container, lessonId, token, isTeacher = false) {
        this.container = container;
        this.lessonId = lessonId;
        this.token = token;
        this.isTeacher = isTeacher;
        this.room = null;
        this.localParticipant = null;
        this.remoteParticipants = new Map();
    }

    async init() {
        // Подключаемся к LiveKit серверу
        this.room = new LiveKit.Room();
        
        this.room.on(LiveKit.RoomEvent.TrackSubscribed, this.onTrackSubscribed.bind(this));
        this.room.on(LiveKit.RoomEvent.ParticipantConnected, this.onParticipantConnected.bind(this));
        this.room.on(LiveKit.RoomEvent.ParticipantDisconnected, this.onParticipantDisconnected.bind(this));
        
        await this.room.connect('wss://your-livekit-server.com', this.token);
        this.localParticipant = this.room.localParticipant;
        
        if (this.isTeacher) {
            // Учитель включает камеру и микрофон
            await this.localParticipant.setCameraEnabled(true);
            await this.localParticipant.setMicrophoneEnabled(true);
        }
        
        this.render();
    }
    
    onTrackSubscribed(track, publication, participant) {
        // Добавляем видео участника на страницу
        if (track.kind === 'video') {
            const element = document.getElementById(`video-${participant.identity}`);
            if (element) {
                track.attach(element);
            }
        }
    }
    
    onParticipantConnected(participant) {
        this.addParticipantVideo(participant);
    }
    
    onParticipantDisconnected(participant) {
        const videoElement = document.getElementById(`video-${participant.identity}`);
        if (videoElement) videoElement.remove();
    }
    
    addParticipantVideo(participant) {
        const videoGrid = document.getElementById('video-grid');
        const wrapper = document.createElement('div');
        wrapper.className = 'video-wrapper';
        wrapper.id = `wrapper-${participant.identity}`;
        wrapper.innerHTML = `
            <video id="video-${participant.identity}" autoplay muted="${participant.identity === this.room.localParticipant?.identity}"></video>
            <div class="participant-name">${participant.identity}</div>
            <div class="hand-${participant.identity} hidden">✋ Рука поднята</div>
        `;
        videoGrid.appendChild(wrapper);
    }
    
    render() {
        this.container.innerHTML = `
            <div class="virtual-class">
                <div class="controls">
                    ${this.isTeacher ? `
                        <button id="toggle-camera">🎥 Камера</button>
                        <button id="toggle-mic">🎤 Микрофон</button>
                        <button id="share-screen">🖥 Демонстрация</button>
                        <button id="start-poll">📊 Опрос</button>
                        <button id="whiteboard">✏️ Доска</button>
                        <button id="start-recording">🔴 Запись</button>
                    ` : `
                        <button id="raise-hand">✋ Поднять руку</button>
                        <button id="request-mic">🎤 Попросить микрофон</button>
                    `}
                    <button id="show-chat">💬 Чат</button>
                    <button id="leave-class">🚪 Выйти</button>
                </div>
                
                <div id="video-grid" class="video-grid"></div>
                
                <div id="chat-panel" class="chat-panel hidden">
                    <div id="chat-messages" class="chat-messages"></div>
                    <input type="text" id="chat-input" placeholder="Напишите сообщение...">
                    <button id="send-chat">Отправить</button>
                </div>
                
                <div id="poll-panel" class="poll-panel hidden">
                    <h4>Опрос</h4>
                    <div id="poll-options"></div>
                    <button id="submit-poll">Голосовать</button>
                </div>
            </div>
        `;
        
        this.attachEventListeners();
    }
    
    attachEventListeners() {
        if (this.isTeacher) {
            document.getElementById('toggle-camera')?.addEventListener('click', async () => {
                const enabled = this.localParticipant.isCameraEnabled;
                await this.localParticipant.setCameraEnabled(!enabled);
            });
            
            document.getElementById('toggle-mic')?.addEventListener('click', async () => {
                const enabled = this.localParticipant.isMicrophoneEnabled;
                await this.localParticipant.setMicrophoneEnabled(!enabled);
            });
            
            document.getElementById('share-screen')?.addEventListener('click', async () => {
                await this.localParticipant.setScreenShareEnabled(true);
            });
            
            document.getElementById('start-poll')?.addEventListener('click', () => {
                this.createPoll();
            });
            
            document.getElementById('whiteboard')?.addEventListener('click', () => {
                this.openWhiteboard();
            });
        } else {
            document.getElementById('raise-hand')?.addEventListener('click', () => {
                this.raiseHand();
            });
        }
        
        document.getElementById('show-chat')?.addEventListener('click', () => {
            const panel = document.getElementById('chat-panel');
            panel.classList.toggle('hidden');
        });
        
        document.getElementById('send-chat')?.addEventListener('click', () => {
            this.sendChatMessage();
        });
        
        document.getElementById('leave-class')?.addEventListener('click', () => {
            this.leave();
        });
    }
    
    raiseHand() {
        // Отправляем сигнал учителю через WebSocket
        const ws = new WebSocket('ws://localhost:8000/ws/class/' + this.lessonId + '/');
        ws.onopen = () => {
            ws.send(JSON.stringify({
                type: 'raise_hand',
                user: this.localParticipant.identity
            }));
        };
    }
    
    sendChatMessage() {
        const input = document.getElementById('chat-input');
        const message = input.value;
        if (!message) return;
        
        const messagesDiv = document.getElementById('chat-messages');
        messagesDiv.innerHTML += `<div><strong>Вы:</strong> ${message}</div>`;
        input.value = '';
        
        // Отправляем через WebSocket
        // ...
    }
    
    leave() {
        this.room?.disconnect();
        this.container.innerHTML = '<div class="card"><h3>Вы покинули урок</h3><a href="/">Вернуться на главную</a></div>';
    }
}

// Экспортируем для использования
window.VirtualClass = VirtualClass;
