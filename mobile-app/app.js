// Tourism Hanoi AI Mobile App
class TourismApp {
    constructor() {
        this.camera = document.getElementById('camera');
        this.canvas = document.getElementById('canvas');
        this.previewImage = document.getElementById('previewImage');
        this.captureBtn = document.getElementById('captureBtn');
        this.uploadBtn = document.getElementById('uploadBtn');
        this.fileInput = document.getElementById('fileInput');
        this.switchCameraBtn = document.getElementById('switchCameraBtn');
        this.retakeBtn = document.getElementById('retakeBtn');
        this.analyzeBtn = document.getElementById('analyzeBtn');
        this.chatBtn = document.getElementById('chatBtn');
        this.chatInput = document.getElementById('chatInput');

        this.cameraSection = document.getElementById('cameraSection');
        this.previewSection = document.getElementById('previewSection');
        this.resultsSection = document.getElementById('resultsSection');
        this.chatHistory = document.getElementById('chatHistory');
        this.chatMessages = document.getElementById('chatMessages');

        this.currentStream = null;
        this.currentFacingMode = 'environment'; // back camera
        this.capturedImage = null;
        this.currentPlace = null;
        this.cameraSupported = false;

        this.init();
    }

    init() {
        this.setupEventListeners();
        this.startCamera();
    }

    setupEventListeners() {
        this.captureBtn.addEventListener('click', () => this.capturePhoto());
        this.uploadBtn.addEventListener('click', () => this.fileInput.click());
        this.fileInput.addEventListener('change', (e) => this.handleFileUpload(e));
        this.switchCameraBtn.addEventListener('click', () => this.switchCamera());
        this.retakeBtn.addEventListener('click', () => this.retakePhoto());
        this.analyzeBtn.addEventListener('click', () => this.analyzePhoto());
        this.chatBtn.addEventListener('click', () => this.sendChatMessage());
        this.chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.sendChatMessage();
        });
    }

    async startCamera() {
        try {
            // Check if browser supports camera
            if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
                throw new Error('Trình duyệt không hỗ trợ camera');
            }

            const constraints = {
                video: {
                    facingMode: this.currentFacingMode,
                    width: { ideal: 1280 },
                    height: { ideal: 720 }
                },
                audio: false
            };

            this.currentStream = await navigator.mediaDevices.getUserMedia(constraints);
            this.camera.srcObject = this.currentStream;
            this.cameraSupported = true;

            this.captureBtn.disabled = false;
            this.switchCameraBtn.disabled = false;
            this.showSuccess('✅ Camera khởi động thành công');
        } catch (error) {
            console.error('Camera error:', error);
            this.cameraSupported = false;
            this.captureBtn.disabled = true;
            this.switchCameraBtn.disabled = true;
            
            let errorMessage = 'Không thể truy cập camera.';
            if (error.name === 'NotAllowedError') {
                errorMessage = 'Bạn chưa cho phép truy cập camera. Vui lòng kiểm tra cài đặt trình duyệt.';
            } else if (error.name === 'NotFoundError') {
                errorMessage = 'Không tìm thấy camera trên thiết bị.';
            } else if (error.message.includes('không hỗ trợ')) {
                errorMessage = 'Trình duyệt không hỗ trợ camera. Vui lòng sử dụng Chrome, Firefox hoặc Safari.';
            }
            
            this.showError(errorMessage);
            this.showError('💡 Bạn có thể tải ảnh từ thư viện thiết bị để thay thế');
        }
    }

    async switchCamera() {
        this.currentFacingMode = this.currentFacingMode === 'environment' ? 'user' : 'environment';

        if (this.currentStream) {
            this.currentStream.getTracks().forEach(track => track.stop());
        }

        await this.startCamera();
    }

    capturePhoto() {
        if (!this.camera.videoWidth) return;

        this.canvas.width = this.camera.videoWidth;
        this.canvas.height = this.camera.videoHeight;

        const ctx = this.canvas.getContext('2d');
        ctx.drawImage(this.camera, 0, 0);

        this.capturedImage = this.canvas.toDataURL('image/jpeg', 0.8);
        this.previewImage.src = this.capturedImage;

        this.showPreview();
    }

    handleFileUpload(event) {
        const file = event.target.files[0];
        if (!file) return;

        // Check file type
        if (!file.type.startsWith('image/')) {
            this.showError('Vui lòng chọn file ảnh (JPG, PNG, etc.)');
            return;
        }

        // Check file size (max 5MB)
        if (file.size > 5 * 1024 * 1024) {
            this.showError('File quá lớn. Vui lòng chọn file nhỏ hơn 5MB');
            return;
        }

        // Read file and display
        const reader = new FileReader();
        reader.onload = (e) => {
            this.capturedImage = e.target.result;
            this.previewImage.src = this.capturedImage;
            this.showPreview();
            this.showSuccess('✅ Tải ảnh thành công');
        };
        reader.onerror = () => {
            this.showError('Lỗi khi đọc file ảnh');
        };
        reader.readAsDataURL(file);

        // Reset input
        this.fileInput.value = '';
    }

    showPreview() {
        this.cameraSection.style.display = 'none';
        this.previewSection.style.display = 'block';
        this.resultsSection.style.display = 'none';
        this.chatHistory.style.display = 'none';
    }

    retakePhoto() {
        this.cameraSection.style.display = 'block';
        this.previewSection.style.display = 'none';
        this.resultsSection.style.display = 'none';
        this.chatHistory.style.display = 'none';
        this.capturedImage = null;
    }

    async analyzePhoto() {
        if (!this.capturedImage) return;

        this.showLoading(true);
        this.resultsSection.style.display = 'block';
        this.chatHistory.style.display = 'none';

        try {
            // Convert base64 to blob
            const response = await fetch(this.capturedImage);
            const blob = await response.blob();

            // Create form data
            const formData = new FormData();
            formData.append('file', blob, 'photo.jpg');

            // Send to backend
            const result = await this.callBackendAPI('/predict', formData);

            if (result.status === 'success') {
                this.currentPlace = result.place_name;
                this.displayResult(result);
                await this.getPlaceInfo(result.place_name);
            } else {
                throw new Error('Không thể nhận diện địa điểm');
            }

        } catch (error) {
            console.error('Analysis error:', error);
            this.showError('Không thể phân tích ảnh. Vui lòng thử lại.');
        } finally {
            this.showLoading(false);
        }
    }

    async callBackendAPI(endpoint, data) {
        const response = await fetch(`http://localhost:8000${endpoint}`, {
            method: 'POST',
            body: data
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    }

    async getPlaceInfo(placeName) {
        try {
            const response = await fetch('http://localhost:8000/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    question: `Cho tôi thông tin về ${placeName}`,
                    place_name: placeName
                })
            });

            if (response.ok) {
                const data = await response.json();
                document.getElementById('placeInfo').textContent = data.answer;
            }
        } catch (error) {
            console.error('Error getting place info:', error);
            document.getElementById('placeInfo').textContent = 'Không thể tải thông tin chi tiết.';
        }
    }

    displayResult(result) {
        document.getElementById('placeName').textContent = this.formatPlaceName(result.place_name);
        document.getElementById('confidence').textContent = `${(result.confidence * 100).toFixed(1)}%`;

        document.getElementById('loadingSpinner').style.display = 'none';
        document.getElementById('resultDetails').style.display = 'block';
    }

    formatPlaceName(name) {
        // Convert folder names to readable Vietnamese names
        const nameMap = {
            'Cầu Long Biên': 'Cầu Long Biên',
            'Chùa Một Cột': 'Chùa Một Cột',
            'Đền Hùng': 'Đền Hùng',
            'Đền Ngọc Sơn': 'Đền Ngọc Sơn',
            'Hồ Hoàn Kiếm': 'Hồ Hoàn Kiếm',
            'Hoàng thành Thăng Long': 'Hoàng thành Thăng Long',
            'Nhà hát lớn': 'Nhà hát Lớn',
            'Nhà thờ lớn': 'Nhà thờ Lớn',
            'Nhà tù Hỏa Lò': 'Nhà tù Hỏa Lò',
            'Phố Cổ': 'Phố Cổ Hà Nội',
            'Quảng trường Ba Đình + Lăng Bác': 'Lăng Bác Hồ',
            'Tháp bút': 'Tháp Bút',
            'Trung tâm Hà Nội': 'Trung tâm Hà Nội',
            'Văn Miếu': 'Văn Miếu Quốc Tử Giám'
        };

        return nameMap[name] || name;
    }

    async sendChatMessage() {
        const message = this.chatInput.value.trim();
        if (!message || !this.currentPlace) return;

        this.addMessage(message, 'user');
        this.chatInput.value = '';

        try {
            const response = await fetch('http://localhost:8000/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    question: message,
                    place_name: this.currentPlace
                })
            });

            if (response.ok) {
                const data = await response.json();
                this.addMessage(data.answer, 'bot');
            } else {
                this.addMessage('Xin lỗi, không thể trả lời câu hỏi này.', 'bot');
            }
        } catch (error) {
            console.error('Chat error:', error);
            this.addMessage('Lỗi kết nối. Vui lòng thử lại.', 'bot');
        }
    }

    addMessage(text, type) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        messageDiv.textContent = text;
        this.chatMessages.appendChild(messageDiv);
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
        this.chatHistory.style.display = 'block';
    }

    showLoading(show) {
        const loadingSpinner = document.getElementById('loadingSpinner');
        if (show) {
            loadingSpinner.style.display = 'block';
            document.getElementById('resultDetails').style.display = 'none';
        } else {
            loadingSpinner.style.display = 'none';
        }
    }

    showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.innerHTML = `<i class="fas fa-exclamation-triangle"></i> ${message}`;

        const resultsSection = document.querySelector('.results-section');
        resultsSection.insertBefore(errorDiv, resultsSection.firstChild);

        setTimeout(() => {
            errorDiv.remove();
        }, 5000);
    }

    showSuccess(message) {
        const successDiv = document.createElement('div');
        successDiv.className = 'success-message';
        successDiv.innerHTML = `<i class="fas fa-check-circle"></i> ${message}`;

        const resultsSection = document.querySelector('.results-section');
        resultsSection.insertBefore(successDiv, resultsSection.firstChild);

        setTimeout(() => {
            successDiv.remove();
        }, 3000);
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Check if running on mobile or localhost
    const isLocalhost = location.hostname === 'localhost' || location.hostname === '127.0.0.1';
    const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);

    if (!isLocalhost && !isMobile) {
        alert('Ứng dụng này được thiết kế cho mobile. Vui lòng truy cập từ điện thoại hoặc sử dụng chế độ responsive.');
    }

    new TourismApp();
});

// Service Worker for PWA (Progressive Web App)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(registration => console.log('SW registered'))
            .catch(error => console.log('SW registration failed'));
    });
}