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
  disabled,
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
  $q.loading.show({message: "Сохранение данных"})
  _.set(guidelines.value, `[0].${props.type}`, guidelines_text.value)

  let r = await api.post(`/api/generator/${activeRpdId.value}/save-additional-info/`, {
    "type": 'guidelines',
    "value": guidelines.value,
  }).then((v) => {
    $q.notify({
      message: "Данные <span class='text-bold'>об методических указаний</span> сохранены!",
      color: "secondary",
      position: "bottom",
      html: true,
    })
  }, (rej) => {
    $q.notify({
      message: "Данные <span class='text-bold'>об методических указаний</span> не сохранены!",
      color: "negative",
      position: "bottom",
      html: true,
    })
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
            :readonly="disabled"
            hint="Для РПД"
            debounce="1000"
            @update:modelValue="saveData"
        />

<!--        <q-btn-->
<!--            class="q-mt-md"-->
<!--            label="Сохранить"-->
<!--            color="primary"-->
<!--            @click="saveData"-->
<!--            v-show="!disabled"-->
<!--        />-->

      </q-card-section>
    </q-card>
  </q-expansion-item>
  <q-separator/>
</template>

<style scoped>

</style>
