<template>
  <v-card>
    <v-card-text>
      <h3>Address</h3>
    </v-card-text>
    <v-divider />
    <v-card-text>
      <h3>{{ gymAddress }}</h3>
    </v-card-text>
    <v-btn class="ma-2" @click="toMap">
      View on Map
    </v-btn>
  </v-card>
</template>

<script>
export default {
  name: "AddressCard",
  props: {
    gymAddress: {
      type: String,
      required: false,
      default: undefined,
    },
  },
  methods: {
    toMap() {
      this.$vuetify.goTo("#map")
    },
  },
}
</script>
