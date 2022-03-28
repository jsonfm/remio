class Video{
    constructor(element){
        this.element = element;
    }

    setImage64(data){
        if(this.element){
            this.element.setAttribute( 
                'src', `data:image/png;base64,${data}`
            );
        }
    }
}

const video = new Video(document.getElementById('video'));

/* SOCKET-IO  */
const socket = io();

socket.on('connect', () => {
    console.log('Conectado!');
});

socket.on('disconnect', () => {
    console.log('Desconectado! ');
})

socket.on('stream', (data) => {
    video.setImage64(data);
})
