<template>
  <v-card class="pb-2">
    <v-card-text>
      <h3>Price Info</h3>
    </v-card-text>
    <v-divider />
    <v-card-text> Drop-in: ${{ dropInPrice }} </v-card-text>
    <v-card-text> Monthly: ${{ monthlyPrice }} </v-card-text>
    <v-btn
      text
      small
      color="error"
      class="ma-2 text-lowercase"
      :href="gymWebsite"
      target="_blank"
    >
      We don't have pricing info for this gym yet, please visit
      <a :href="gymWebsite" target="_blank">their website</a>
      for more information
    </v-btn>
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
}
</script>
