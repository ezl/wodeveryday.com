<template>
  <v-card class="pa-2 mb-3" tile>
    <v-container>
      <v-row>
        <v-col md6 class="d-flex justify-center align-center">
          <v-avatar size="200">
            <!--eslint-disable-next-line vue/html-self-closing-->
            <img :src="gymLogo" />
          </v-avatar>
        </v-col>
        <v-col md6 class="d-flex flex-column justify-center">
          <h1>{{ gymName }}</h1>

          <v-rating
            v-if="gymRating && gymRating != -1"
            v-model="gymRating"
            readonly
            class="mt-2"
            background-color="yellow"
            color="yellow accent-4"
          />
          <v-progress-circular
            v-if="gymRating === undefined && gymRating != -1"
            indeterminate
            color="amber"
          />
        </v-col>
      </v-row>
    </v-container>
  </v-card>
</template>

<script>
export default {
  name: "InfoCard",
  props: {
    gymLogo: {
      type: String,
      required: false,
      default: undefined,
    },
    gymName: {
      type: String,
      required: false,
      default: undefined,
    },
    gymWebsite: {
      type: String,
      required: false,
      default: undefined,
    },
    gymPhoneNumber: {
      type: String,
      required: false,
      default: undefined,
    },
    gymRating: {
      type: Number,
      required: false,
      default: undefined,
    },
  },
  methods: {
    phoneNumberVisible() {
      return (
        this.gymPhoneNumber === undefined ||
        (this.gymPhoneNumber && this.gymPhoneNumber.length > 0)
      )
    },
    copyToClipboard() {
      navigator.clipboard.writeText(this.gymPhoneNumber)
    },
  },
}
</script>
