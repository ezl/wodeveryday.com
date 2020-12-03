<template>
</template>

<script>
  export default {
    name: "index",
    head() {
      return {
        title: 'wodeveryday',
        meta: [
          // hid is used as unique identifier. Do not use `vmid` for it as it will not work
          // {
          //   hid: 'description',
          //   name: 'description',
          //   content: 'My custom description'
          // }
        ]
      }
    },
    mounted() {
      this.$router.push({name: 'index'})
    }
  }
</script>

<style scoped>

</style>
