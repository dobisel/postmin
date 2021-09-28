<a href="/">
  <svg>
    <use xlink:href="#icon-logo"></use>
  </svg>{ title }
</a>
<style lang="sass" type="text/sass" scoped>

$h: $navheight - $gutter * 2

a
  height: $h 
  line-height: $h 
  vertical-align: baseline
  font-size: $fontsize + 20
  font-weight: 700
  svg
    /* Doozak */
    width: $h
    height: $h
    margin-top: $gutter
    margin-right: $gutter

    /* Bazak */
    fill: $logo-color
</style> 
<script>
  export let title;
</script>
