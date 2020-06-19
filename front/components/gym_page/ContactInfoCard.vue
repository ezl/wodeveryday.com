<template>
  <v-card class="pb-2">
    <v-card-text>
      <h3>Contact Info</h3>
    </v-card-text>
    <v-divider />
    <v-btn
      v-show="$store.state.gym_object.website"
      large
      class="ma-2"
      :href="$store.state.gym_object.website"
      target="_blank"
    >
      Visit their website
    </v-btn>
    <v-tooltip v-if="phoneNumberVisible" right>
      <template v-slot:activator="{ on }">
        <v-btn
          large
          class="ml-2 d-block"
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
    <v-tooltip v-if="$store.state.gym_object.email" right>
      <template v-slot:activator="{ on }">
        <v-btn large class="ml-2 d-block" v-on="on" @click="copyToClipboard()">
          {{ $store.state.gym_object.email
          }}<v-icon right>
            mdi-content-copy
          </v-icon>
        </v-btn>
      </template>
      <span>Click to copy</span>
    </v-tooltip>
  </v-card>
</template>

<script>
export default {
  name: "ContactInfoCard",
  computed: {
    gymPhoneNumber: function () {
      return this.$store.state.place_details.formatted_phone_number || ""
    },
    phoneNumberVisible: function () {
      return (
        this.gymPhoneNumber === undefined ||
        (this.gymPhoneNumber && this.gymPhoneNumber.length > 0)
      )
    },
  },
  methods: {
    copyToClipboard() {
      navigator.clipboard.writeText(this.gymPhoneNumber)
    },
  },
}
</script>
