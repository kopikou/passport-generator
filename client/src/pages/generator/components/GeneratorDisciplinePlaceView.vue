<script setup lang="ts">

import {onBeforeMount, ref, watch} from "vue";
import {bi0CircleFill} from "@quasar/extras/bootstrap-icons";
import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import _ from "lodash";
import QSelectFilterable from "components/QSelectFilterable.vue";
import {api} from "boot/axios";
import {useQuasar} from "quasar";

const $q = useQuasar()
const generatorViewStore = useGeneratorViewStore();

const {
  otherDiscipline,
  activeRpdId,
  disciplinePlace,
  additionalInfo,
  disabled,
} = storeToRefs(generatorViewStore)

const precedence = ref([])
const subsequent = ref([])

const listDiscipline = ref(otherDiscipline)
const filteredDiscipline = ref(listDiscipline.value)

async function savePrecSubDiscipline() {
  $q.loading.show({message: "Сохранение"})
  let r = await api.post(`api/generator/${activeRpdId.value}/save-additional-info/`, {
    type: "disciplinePlace",
    value: {
      "precedence": precedence.value,
      "subsequent": subsequent.value,
    }
  }).then((v) => {
    $q.notify({
      message: "Данные <span class='text-bold'>о месте дисциплины в структуре ООП</span> сохранены!",
      color: "secondary",
      position: "bottom",
      html: true,
    })

    let key = _.findKey(additionalInfo.value, (x) => x.id == v.data.id)
    _.set(additionalInfo.value, `[${key}].value.precedence`, precedence.value)
    _.set(additionalInfo.value, `[${key}].value.subsequent`, subsequent.value)
  }, (rej) => {
    $q.notify({
      message: "Данные <span class='text-bold'>о месте дисциплины в структуре ООП</span> не сохранены!",
      color: "negative",
      position: "bottom",
      html: true,
    })
  })

  $q.loading.hide()
}

watch(disciplinePlace, () => {
  precedence.value = disciplinePlace.value[0]?.value['precedence'] || []
  subsequent.value = disciplinePlace.value[0]?.value['subsequent'] || []
})

onBeforeMount(() => {
  precedence.value = disciplinePlace.value[0]?.value['precedence'] || []
  subsequent.value = disciplinePlace.value[0]?.value['subsequent'] || []
})


</script>

<template>
  <div>
    <div style="width: 95%">
      <span class="text-h6 q-pl-lg">Место дисциплины в структуре ООП</span>
      <p></p>
      <q-separator class="q-mt-md q-mb-md"/>
      <q-select-filterable
        label="Обеспечивающие (предшествующие) дисциплины и практики"
        v-model="precedence"
        option-label="dis"
        option-value="disid"
        stack-label
        filled
        use-chips
        clearable
        multiple
        map-options
        emit-value
        :options="otherDiscipline"
        :readonly="disabled"
        @update:modelValue="savePrecSubDiscipline"
      />
      <br/>
      <q-select-filterable
        label="Обеспечиваемые (последующие) дисциплины и практики"
        v-model="subsequent"
        option-label="dis"
        option-value="disid"
        stack-label
        filled
        use-chips
        clearable
        multiple
        map-options
        emit-value
        :options="otherDiscipline"
        :readonly="disabled"
        @update:modelValue="savePrecSubDiscipline"
      />
      <!--      <q-btn label="Сохранить" color="primary" class="q-mt-sm" @click="savePrecSubDiscipline" v-show="!disabled"/>-->
    </div>
  </div>
</template>

<style scoped>

</style>
