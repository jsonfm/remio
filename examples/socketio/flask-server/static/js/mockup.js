const socket = io();
const image = document.getElementById('image');

/**
 * Adds a MIME header to a base64 png image.
 * @param {string} b64 - png image base64 encoded.
 * @returns {string}
 */
 function addMIMEjpeg(b64){
    if(!b64.includes('data:')){
        return `data:image/jpeg;base64,${b64}`;
    }else{
        return b64;
    }
}


socket.on('connect', () => {
    console.log('conectado...')
})

socket.on('disconnect', () => {
    console.log('desconectado...')
})

socket.on('stream', (data) => {
    b64 = addMIMEjpeg(data);
    image.src = b64;
});