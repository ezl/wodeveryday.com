<template>
  <div>
    <h1>About</h1>
  </div>
</template>

<script>
  export default {
    name: "about",
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
  }
</script>

<style scoped>

</style>
