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
const guidelines = ref<string>('')

async function saveData() {
  $q.loading.show("Сохранение данных")
  let r = await api.post(`/api/generator/${activeRpdId.value}/save-additional-info/`, {
    type: `guidelines_${props.type}`,
    value: {
      "text": guidelines.value,
    }
  })
  let key = _.findKey(additionalInfo.value, (x) => x.id == r.data.id)
  if (key === undefined) {
    additionalInfo.value.push(r.data)
  } else {
    _.set(additionalInfo.value, `[${key}].value['text']`, r.data.value['text'])
  }
  $q.loading.hide()
}

watch(additionalInfo, () => {
  guidelines.value = _.filter(additionalInfo.value, (x) => x.type == `guidelines_${props.type}`)[0]?.value['text']
})

onBeforeMount(() => {
  guidelines.value = _.filter(additionalInfo.value, (x) => x.type == `guidelines_${props.type}`)[0]?.value['text']
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
            v-model="guidelines"
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
