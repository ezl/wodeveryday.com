<template>
  <v-col cols="12" sm="8" md="4">
    <v-card class="pa-4 elevation-12">
      <v-autocomplete
        v-model="selectedItem"
        :items="getSearchableList"
        :loading="isLoading"
        color="white"
        hide-no-data
        hide-selected
        placeholder="Start typing to Search"
        return-object
        @change="selectSubitemPrefetch(null, selectedItem)"
      />
    </v-card>
  </v-col>
</template>

<script>
export default {
  name: "GeographySearchBar",
  props: {
    itemList: {
      type: Object,
      required: false,
      default: Object,
    },
    selectSubitemPrefetch: {
      type: Function,
      default: () => {},
    },
  },
  data() {
    return {
      selectedItem: undefined,
    }
  },
  computed: {
    getSearchableList: function () {
      if (!this.itemList) return []
      let searchableList = this.flat(Object.values(this.itemList))
      return searchableList
    },
    isLoading: function () {
      return (
        this.itemList === undefined || Object.values(this.itemList).length === 0
      )
    },
  },
  methods: {
    flat(input, depth = 1, stack) {
      const validStack = stack || []
      for (let item of input) {
        if (item instanceof Array && depth > 0) {
          this.flat(item, depth - 1, validStack)
        } else {
          // TODO: remove this tech debt
          if (item && typeof item !== "string") item = item[0]
          validStack.push(item)
        }
      }

      return validStack
    },
  },
}
</script>
