
<style type="text/sass" scoped>
  @import 'styles/grid'

</style>
<script>
import { onMount } from 'svelte';

/* Properties */
export let loading = true;

onMount(async function() {
  loading = false;
});

</script>
