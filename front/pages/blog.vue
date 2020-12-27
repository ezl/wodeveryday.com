<template>
  <h2>
    Blog
  </h2>
</template>

<script>
  export default {
    name: "blog",
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
