<template>
  <v-card class="mb-3">
    <v-card-text>
      <h3 class="text-uppercase">
        <nuxt-link to="/gyms">
          <v-btn text>
            Gyms
          </v-btn>
        </nuxt-link>
        >
        <v-btn text>
          {{ $store.state.current_affiliate.city }}
        </v-btn>
        >
        <v-btn text>
          {{ gymName }}
        </v-btn>
      </h3>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: "Drilldown",
  props: {
    gymName: {
      type: String,
      required: true,
      default: undefined,
    },
  },
}
</script>
