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
        <v-col md6>
          <h1>{{ gymName }}</h1>
          <v-btn large class="mt-2" :href="gymWebsite" target="_blank">
            Visit their website
          </v-btn>

          <v-tooltip v-if="phoneNumberVisible()" right>
            <template v-slot:activator="{ on }">
              <v-btn
                id="phone_field"
                large
                class="my-2 d-block"
                :loading="gymPhoneNumber === undefined"
                v-on="on"
                @click="copyToClipboard()"
              >
                {{ gymPhoneNumber
                }}<v-icon right>
                  mdi-content-copy
                </v-icon>
              </v-btn>
            </template>
            <span>Click to copy</span>
          </v-tooltip>

          <v-rating
            v-if="gymRating && gymRating != -1"
            v-model="gymRating"
            readonly
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
  name: "GymInfoCard",
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
