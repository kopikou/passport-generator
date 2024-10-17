<script setup lang="ts">

import {onBeforeMount, ref, watch} from "vue";
import {api} from "boot/axios";
import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import _ from "lodash";
import {useQuasar} from "quasar";

const generatorViewStore = useGeneratorViewStore();

const {
  activeRpdId,
  additionalInfo,
  guidelines,
} = storeToRefs(generatorViewStore)

const props = defineProps({
  label: {
    required: true,
  },
  type: {
    required: true,
  }
})
const $q = useQuasar()
const guidelines_text = ref<string>('')

async function saveData() {
  $q.loading.show("Сохранение данных")
  _.set(guidelines.value, `[0].${props.type}`, guidelines_text.value)
  console.log(guidelines.value)
  let r = await api.post(`/api/generator/${activeRpdId.value}/save-additional-info/`, {
    "type": 'guidelines',
    "value": guidelines.value,
  })
  $q.loading.hide()
}

watch(additionalInfo, () => {
  guidelines_text.value = _.get(guidelines.value, `[0].${props.type}`)

})

onBeforeMount(() => {
  guidelines_text.value = _.get(guidelines.value, `[0].${props.type}`)
})

</script>

<template>
  <q-expansion-item
      :label=props.label
  >
    <q-card>
      <q-card-section>

        <q-input
            label="Методические указания"
            type="textarea"
            filled
            v-model="guidelines_text"
        />

        <q-btn
            class="q-mt-md"
            label="Сохранить"
            color="primary"
            @click="saveData"
        />

      </q-card-section>
    </q-card>
  </q-expansion-item>
  <q-separator/>
</template>

<style scoped>

</style>
