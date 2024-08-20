<script setup lang="ts">

import {PlanIndicatorData} from "src/types";
import {ref} from "vue";

const props = defineProps({
  data: {
    type: Object as ()=>PlanIndicatorData,
    required: true,
  }
})

const know = ref(null)
const able = ref(null)
const own = ref(null)
const criteria = ref(null)
const methods = ref(null)

</script>

<template>
  <div class="q-pb-md">
    <span class="text-subtitle1">{{ data.indicator_index }} {{ data.indicator }}</span>
    <div class="indicators-form row justify-between q-gutter-md">
      <q-input
          filled
          label="Знать"
          stack-label
          type="textarea"
          class="col"
          v-model="know"
      />
      <q-input
          filled
          label="Уметь"
          stack-label
          type="textarea"
          class="col"
          v-model="able"
      />
      <q-input
          filled
          label="Владеть"
          stack-label
          type="textarea"
          class="col"
          v-model="own"
      />
      <q-input
          filled
          label="Критерии оценивания"
          stack-label
          type="textarea"
          class="col"
          v-model="criteria"
      />
      <q-input
          filled
          label="Средства (методы) оценивания промежуточной аттестации"
          stack-label
          type="textarea"
          class="col"
          v-model="methods"
      />
    </div>
    <div class="flex justify-end q-mt-md">
      <q-btn label="Сохранить" color="primary"/>
    </div>
  </div>
</template>

<style scoped lang="scss">
.indicators-form {
  > label {
    flex-basis: 400px;
  }
}
</style>
