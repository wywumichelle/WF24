;*************************************************
; mask_9.ncl
;
; Concepts illustrated:
;   - Drawing the Mississippi River Basin using data from a shapefile
;   - Masking a data array based on a geographical area
;   - Attaching markers to a map
;   - Attaching polylines to a map plot
;   - Drawing a lat/lon grid using markers
;   - Copying coordinate arrays from one variable to another
;
;*************************************************
;
; These files are loaded by default in NCL V6.2.0 and newer
; load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
; load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
; load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"

load "./shapefile_utils.ncl"
begin
  f1   = addfile("/work/04380/wenying/lonestar/share/ST/CMIP6/historical/Amon/pr/pr_Amon_ACCESS-CM2_historical_3ensmean_global-1_185001-201412.nc","r")
  data   = f1->pr(0,:,:)

  shp_filename1= "./cb_2018_us_state_500k/cb_2018_us_state_500k.shp"



;--- select states.
  opt             = True
  opt@debug       = True
  opt@shape_var   = "NAME"
  opt@shape_names = (/"Texas"/)
  data_mask  = shapefile_mask_data(data,shp_filename1,opt)
  data_mask  = where(ismissing(data_mask),0,1)
  printVarSummary(data_mask)
  delete_VarAtts(data_mask,(/"_FillValue","time","cell_methods","cell_measures","history","missing_value"/))
  data_mask@long_name = "Texas mask"
  data_mask@units    = " "
  data_mask@standard_name = "Texas_Global-1"
  data_mask@comment = "1=Texas,0=non-Texas"
  copy_VarCoords(data,data_mask)    
;-----------------
  system("rm -f StateTexas_global-1.nc")
  fo = addfile("StateTexas_global-1.nc","c")
  fo->mask = data_mask

;---Start the graphics
  wks  = gsn_open_wks("png","mask_StateTexas_global-1")        ; send graphics to PNG file

  res                      = True     ; plot mods desired
  res@cnFillOn             = True     ; turn on color fill
  res@cnLinesOn            = False    ; turn off contour lines
  res@gsnDraw             = False          ; don't draw plot yet
  res@gsnFrame            = False          ; don't advance frame yet
  res@cnFillMode          = "RasterFill"
  res@gsnAddCyclic        = False          ; Don't add a cyclic point.

  res@mpDataBaseVersion   = "MediumRes"    ; slightly better resolution

  res@mpProjection        = "LambertConformal"    ; choose projection
  res@mpLambertParallel1F = 33          ; first parallel
  res@mpLambertParallel2F = 45          ; second parallel
  res@mpLambertMeridianF  = -98         ; meridian

  res@mpLimitMode         = "Corners"   ; corner method of zoom
  res@mpLeftCornerLatF    = 22          ; left corner
  res@mpLeftCornerLonF    = -120        ; left corner
  res@mpRightCornerLatF   = 49         ; right corner
  res@mpRightCornerLonF   = -64         ; right corner


  res@tiMainString        = "Data mask with Texas"

;---Create contours over map.
  map_data = gsn_csm_contour_map(wks,data_mask,res)

;---Resources for polyline
  lnres                  = True
  lnres@gsLineColor      = "blue"
  lnres@gsLineThicknessF = 2.0            ; 2x thickness

;---Attach MRB outline to map.
  id_map = gsn_add_shapefile_polylines(wks,map_data,shp_filename1,lnres)

;---Draw plot and advance frame
  draw(map_data)
  frame(wks)

end

