<template>
    <youtube :player-vars="{ autoplay: 1 }" :video-id="video_id" />
</template>

<script>
export default {
    data() {
        return {
            video_id: '7OlP1YyKRdg'
        }
    }
}
</script>

<style>

</style>