const cam = document.getElementById('cam')

// encapsulamento
const startVideo = () => {
    navigator.mediaDevices.enumerateDevices()
        .then(devices => {
            if (Array.isArray(devices)) {
                devices.forEach(device => {
                    if (device.kind === 'videoinput') {
                        if (device.label.includes('VX-2000')) {
                            navigator.getUserMedia(
                                {
                                    video: {
                                        deviceId: device.deviceId
                                    }
                                },
                                stream => cam.srcObject = stream,
                                error => console.error(error)
                            )
                        }
                    }
                })
            }
        })
}

//será carregado primeiro antes do uso da biblioteca
Promise.all([
    faceapi.nets.tinyFaceDetector.loadFromUri('/assets/lib/face-api/models'), // Desenha um quadrado em volta do rosto
    faceapi.nets.faceLandmark68Net.loadFromUri('/assets/lib/face-api/models'), //Desennha traços no rosto
    faceapi.nets.faceRecognitionNet.loadFromUri('/assets/lib/face-api/models'), //Reconhecimento do rosoto
    faceapi.nets.faceExpressionNet.loadFromUri('/assets/lib/face-api/models'),
    faceapi.nets.ageGenderNet.loadFromUri('/assets/lib/face-api/models'), //Reconhe a idadee e genero
    faceapi.nets.ssdMobilenetv1.loadFromUri('/assets/lib/face-api/models'), // utilizada para detectar rostos
]).then(startVideo)

cam.addEventListener('play', async () => {
    
})