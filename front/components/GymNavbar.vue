<template>
  <v-card-text v-if="navbarActive" class="text-center">
    <h3
      v-for="(name, index) in navbarOptions"
      :key="index"
      class="text-uppercase d-inline-block"
    >
      <v-btn text @click="toElement(index)">
        {{ name }}
      </v-btn>
      <span v-if="index != navbarOptions.length - 1" class="px-2">
        |
      </span>
    </h3>
  </v-card-text>
</template>

<script>
export default {
  name: "GymNavbar",
  props: {
    navbarOptions: {
      type: Array,
      required: true,
      default: Array,
    },
    gotoElements: {
      type: Array,
      default: Array,
    },
    navbarActive: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    toElement(index) {
      this.$vuetify.goTo(this.gotoElements[index])
    },
  },
}
</script>
