<script setup lang="ts">

import {PlanIndicatorData} from "src/types";
import {onBeforeMount, ref} from "vue";
import {api} from "boot/axios";

const props = defineProps({
  data: {
    type: Object as () => PlanIndicatorData,
    required: true,
  }
})

const know = ref(null)
const able = ref(null)
const own = ref(null)
const criteria = ref(null)
const methods = ref(null)

async function saveData() {
  let r = await api.post('/api/generator/save-discipline-indicator/', {
    indicator_id: props.data.id,
    planlineid_id: props.data.planlineid_id,
    know: know.value,
    able: able.value,
    own: own.value,
    criteria: criteria.value,
    methods: methods.value,
  })

  props.data.discipline_indicator[0] = r.data
}

onBeforeMount(() => {
  if (props.data.discipline_indicator.length != 0) {
    know.value = props.data.discipline_indicator[0].know || null
    able.value = props.data.discipline_indicator[0].able || null
    own.value = props.data.discipline_indicator[0].own || null
    criteria.value = props.data.discipline_indicator[0].criteria || null
    methods.value = props.data.discipline_indicator[0].methods || null
  }
})

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
      <q-btn label="Сохранить" color="primary" @click="saveData"/>
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
