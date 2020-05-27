<template>
  <v-card class="pb-2">
    <v-card-text>
      <h3>Price Info</h3>
    </v-card-text>
    <v-divider />
    <v-card-text v-if="dropInPrice !== $store.state.constants.DEFAULT_PRICE">
      Drop-in: ${{ dropInPrice }}
    </v-card-text>
    <v-card-text v-if="monthlyPrice !== $store.state.constants.DEFAULT_PRICE">
      Monthly: ${{ monthlyPrice }}
    </v-card-text>
    <v-card-text v-if="pricingUnavailableMessageVisible" class="ma-2 red--text">
      We don't have pricing info for this gym yet, please visit
      <a :href="gymWebsite" target="_blank">their website</a>
      for more information
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: "PriceCard",
  props: {
    dropInPrice: {
      type: String,
      required: false,
      default: "??.??",
    },
    monthlyPrice: {
      type: String,
      required: false,
      default: "??.??",
    },
    gymWebsite: {
      type: String,
      required: false,
      default: "#",
    },
  },
  computed: {
    pricingUnavailableMessageVisible: function () {
      return (
        this.dropInPrice === this.$store.state.constants.DEFAULT_PRICE &&
        this.monthlyPrice === this.$store.state.constants.DEFAULT_PRICE
      )
    },
  },
}
</script>
