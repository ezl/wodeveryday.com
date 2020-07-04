<template>
  <v-card>
    <v-card-text>
      <h3>Address</h3>
    </v-card-text>
    <v-divider />
    <v-card-text>
      <h3
        itemprop="address"
        itemscope
        itemtype="https://schema.org/PostalAddress"
      >
        <span itemprop="streetAddress">{{
          $store.state.gym_object.address
        }}</span>
        <span itemprop="postalCode">{{ $store.state.gym_object.zip }}</span>
        <span itemprop="addressCountry">{{
          $store.state.gym_object.country
        }}</span>
      </h3>
    </v-card-text>
    <v-btn class="ma-2" @click="toMap">
      View on Map
    </v-btn>
  </v-card>
</template>

<script>
export default {
  name: "AddressCard",
  methods: {
    toMap() {
      this.$vuetify.goTo("#map")
    },
  },
}
</script>
